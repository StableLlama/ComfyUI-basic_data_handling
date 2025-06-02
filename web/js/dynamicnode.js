/**
 * ComfyUI basic data handling.
 * Copyright (C) 2025 StableLlama
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

/**
 * Purpose: Manage dynamic input nodes in ComfyUI.
 * Inspired by cozy_ex_dynamic
 */

import { app } from "../../../scripts/app.js";

const TypeSlot = {
    Input: 1,
    Output: 2
};

const TypeSlotEvent = {
    Connect: true,
    Disconnect: false
};

app.registerExtension({
    name: 'Basic data handling: dynamic input',
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // Filter: Only process nodes with class names starting with "Basic data handling:"
        if (!nodeType.comfyClass.startsWith('Basic data handling:')) {
            return;
        }

        const combinedInputData = {
            ...nodeData?.input?.required ?? {},
            ...nodeData?.input?.optional ?? {}
        }
        const combinedInputDataOrder = [
            ...nodeData?.input_order?.required ?? [],
            ...nodeData?.input_order?.optional ?? []
        ];

        /** Array of (generic) dynamic inputs. */
        const dynamicInputs = [];
        /** Array of groups of (generic) dynamic inputs. */
        const dynamicInputGroups = [];
        for (const name of combinedInputDataOrder) {
            const widgetType = combinedInputData[name][1]?.widgetType;
            const dynamic = combinedInputData[name][1]?._dynamic;
            const dynamicGroup = combinedInputData[name][1]?._dynamicGroup ?? 0;

            if (dynamic) {
                let matcher;

                switch (dynamic) {
                    case 'number':
                        matcher = new RegExp(`^(${name.replace(/\d*$/, '')})(\\d+)$`);
                        break;

                    case 'letter':
                        matcher = new RegExp(`^()([a-zA-Z])$`);
                        break;

                    default:
                        continue;
                }
                const baseName = name.match(matcher)?.[1] ?? name;
                const dynamicType = combinedInputData[name][0];
                if (dynamicInputGroups[dynamicGroup] === undefined) {
                    dynamicInputGroups[dynamicGroup] = [];
                }
                dynamicInputGroups[dynamicGroup].push(
                    dynamicInputs.length
                )
                dynamicInputs.push({name, baseName, matcher, dynamic, dynamicType, dynamicGroup, widgetType});
            }
        }
        if (dynamicInputs.length === 0) {
            return;
        }

        /**
         * Utility functions for dynamic input operations
         */
            // Check if an input is dynamic
        const isDynamicInput = (inputName) =>
                dynamicInputs.some((di) => di.matcher.test(inputName));

        // Update inputs' slot indices after reordering
        const updateSlotIndices = (node) => {
            node.inputs.forEach((input, index) => {
                input.slot_index = index;
                if (input.isConnected) {
                    const link = node.graph._links.get(input.link);
                    if (link) {
                        link.target_slot = index;
                    } else {
                        console.error(`Input ${index} has an invalid link.`);
                    }
                }
            });
        };

        // Get default value for widget based on its type
        const getWidgetDefaultValue = (widget) => {
            switch (widget.type) {
                case 'number':
                    return 0;
                case 'combo':
                    return widget.options?.[0] || '';
                case 'text':
                case 'string':
                default:
                    return '';
            }
        };

        // Check if a dynamic input is empty (not connected and widget has default value)
        const isDynamicInputEmpty = (node, inputIndex) => {
            const input = node.inputs[inputIndex];
            if (input.isConnected) return false;

            if (input.widget) {
                const widget = node.widgets.find(w => w.name === input.widget.name);
                return widget?.value === getWidgetDefaultValue(widget);
            }
            return true;
        };

        // Find if input is the last of its base name group
        const isLastDynamicInput = (node, idx, baseName) => {
            let isLast = true;
            for (let i = idx + 1; i < node.inputs.length; i++) {
                isLast &&= !node.inputs[i].name.startsWith(baseName);
            }
            return isLast;
        };

        // Remove widget associated with an input
        const removeWidgetForInput = (node, inputIdx) => {
            if (node.inputs[inputIdx].widget !== undefined) {
                const widgetIdx = node.widgets.findIndex((w) => w.name === node.inputs[inputIdx].widget.name);
                node.widgets.splice(widgetIdx, 1);
                node.widgets_values?.splice(widgetIdx, 1);
            }
        };

        // Add helper method to get dynamic group for an input name
        nodeType.prototype.getDynamicGroup = function(inputName) {
            // Find the dynamicGroup by matching the baseName with input name
            for (const di of dynamicInputs) {
                if (inputName.startsWith(di.baseName)) {
                    return di.dynamicGroup;
                }
            }
            return undefined;
        };

        /**
         * Add a widget with standard configuration.
         * @param {string} name - The name of the widget.
         * @param {string} widget_type - The type of widget.
         * @returns {object} The created widget.
         */
        const addStandardWidget = function(name, widget_type) {
            return this.addWidget(widget_type, name, '', () => {}, {});
        };

        // Add helper method to insert input at a specific position
        nodeType.prototype.addInputAtPosition = function (name, input_type, widget_type, position, isWidget, shape) {
            // Add widget if needed
            if (isWidget) {
                addStandardWidget.call(this, name, widget_type);

                const GET_CONFIG = Symbol();
                this.addInput(name, input_type, {
                    shape,
                    widget: {name, [GET_CONFIG]: () =>{}}
                });
            } else {
                this.addInput(name, input_type, {shape}); // Add new input without widget
            }

            // Position the input at the desired location
            const newInput = this.inputs.pop(); // Get the newly added input (last item)
            this.inputs.splice(position, 0, newInput); // Place it at the desired position
            updateSlotIndices(this); // Update indices
            return newInput;
        };

        // flag to prevent loops. It is ok to be "global" as the code is not
        // running in parallel.
        let isProcessingConnection = false;

        /**
         * Utility: Handle when a dynamic input becomes empty (disconnected or empty widget value).
         * @param {ComfyNode} node - The node with the empty input.
         */
        const handleEmptyDynamicInput = function() {
            // Process each input to check for empty dynamic inputs
            for (let idx = 0; idx < this.inputs.length; idx++) {
                const input = this.inputs[idx];

                // Skip if not a dynamic input
                if (!isDynamicInput(input.name)) {
                    continue;
                }

                // Check if this input is empty
                if (!isDynamicInputEmpty(this, idx)) {
                    continue;
                }

                // Get information about this dynamic input group
                const dynamicGroup = this.getDynamicGroup(input.name);
                const baseName = dynamicInputs[dynamicInputGroups[dynamicGroup][0]].baseName;

                // Don't remove if it's the last dynamic input of its type
                if (isLastDynamicInput(this, idx, baseName)) {
                    continue;
                }

                // Move the empty input to the end
                for (let i = idx + 1; i < this.inputs.length; i++) {
                    this.swapInputs(i - 1, i);
                }

                // Remove the input that's now at the end
                const lastIdx = this.inputs.length - 1;
                removeWidgetForInput(this, lastIdx);
                this.removeInput(lastIdx);

                // Adjust idx to check the current position again (which now has a new input)
                idx--;
            }

            // Renumber all dynamic inputs to ensure proper ordering
            for (const groupIdx in dynamicInputGroups) {
                for (const memberIdx of dynamicInputGroups[groupIdx]) {
                    const baseName = dynamicInputs[memberIdx].baseName;
                    const dynamic = dynamicInputs[memberIdx].dynamic;
                    this.renumberDynamicInputs(baseName, dynamicInputs, dynamic);
                }
            }
        };

        /**
         * Utility: Handle when a dynamic input becomes active (connected or non-empty widget value).
         * @param {ComfyNode} node - The node with the activated input.
         * @param {number} dynamicGroup - The dynamic group to handle.
         */
        const handleDynamicInputActivation = function(dynamicGroup) {
            // Get information about dynamic inputs
            const {
                slots: dynamicSlots,
                groupConnected: dynamicGroupConnected
            } = this.getDynamicSlots();

            // Ensure all widget-based inputs have actual widgets
            // This is important when loading workflows
            for (const slot of dynamicSlots) {
                if (slot.isWidget && this.widgets &&
                    !this.widgets.some((w) => w.name === slot.name)) {
                    this.addWidget(
                        this.inputs[slot.index].type,
                        slot.name,
                        '',
                        ()=>{},
                        {}
                    );
                }
            }

            // If all inputs in this group are active, we need to add a new empty one
            const hasEmptyInput = dynamicGroupConnected[dynamicGroup]?.some(isActive => !isActive);

            if (!hasEmptyInput) {
                // Find position for the new input (after the last one in this group)
                const groupSlots = dynamicSlots.filter(slot => slot.dynamicGroup === dynamicGroup);
                const lastDynamicIdx = groupSlots.length > 0
                    ? Math.max(...groupSlots.map(slot => slot.index))
                    : -1;

                // Add a new empty input for this group
                this.addNewDynamicInputForGroup(dynamicGroup, lastDynamicIdx);
            }

            // Ensure the canvas is updated

            this.setDirtyCanvas(true, true);
        };

        // Override onConnectionsChange: Handle connections for dynamic inputs
        const onConnectionsChange = nodeType.prototype.onConnectionsChange;
        nodeType.prototype.onConnectionsChange = function (type, slotIndex, isConnected, link, ioSlot) {
            // Call the original method first
            const result = onConnectionsChange?.apply(this, arguments);

            // Only process input connections for dynamic inputs
            const isInput = type === TypeSlot.Input;
            const isDynamic = isInput && isDynamicInput(this.inputs[slotIndex].name);

            // Skip if not an input, already processing, or not a dynamic input
            if (!isInput || isProcessingConnection || !isDynamic) {
                return result;
            }

            // Prevent recursive processing
            isProcessingConnection = true;

            // Get the dynamic group for this input
            const dynamicGroup = this.getDynamicGroup(this.inputs[slotIndex].name);

            // Handle connection or disconnection event
            if (isConnected === TypeSlotEvent.Connect) {
                // Input was connected
                handleDynamicInputActivation.call(this, dynamicGroup);
            } else if (isConnected === TypeSlotEvent.Disconnect) {
                // Input was disconnected
                handleEmptyDynamicInput.call(this);
            }

            isProcessingConnection = false;
            return result;
        };

        const onConnectInput = nodeType.prototype.onConnectInput;
        nodeType.prototype.onConnectInput = function(inputIndex, outputType, outputSlot, outputNode, outputIndex) {
            const result = onConnectInput?.apply(this, arguments) ?? true;

            if (this.inputs[inputIndex].isConnected) {
                const pre_isProcessingConnection = isProcessingConnection;
                isProcessingConnection = true;
                this.disconnectInput(inputIndex, true);
                isProcessingConnection = pre_isProcessingConnection;
            }
            return result;
        }

        const onRemoved = nodeType.prototype.onRemoved;
        nodeType.prototype.onRemoved = function () {
            const result = onRemoved?.apply(this, arguments);

            // When this is called, the input links are already removed - but
            // due to the implementation of the remove() method it might not
            // have worked with the dynamic inputs. So we need to fix it here.
            for (let i = this.inputs.length-1; i >= 0; i--) {
                if ( this.inputs[i].isConnected) {
                    this.disconnectInput(i, true);
                }
            }

            return result;
        }

        /**
         * Utility: Find input index for a widget by name.
         * @param {ComfyNode} node - The node containing the widget.
         * @param {string} widgetName - Name of the widget to find.
         * @returns {number} Index of the input associated with the widget, or -1 if not found.
         */
        const findInputIndexForWidget = (node, widgetName) => {
            for (let i = 0; i < node.inputs.length; i++) {
                if (node.inputs[i].widget && node.inputs[i].widget.name === widgetName) {
                    return i;
                }
            }
            return -1;
        };

        const onWidgetChanged = nodeType.prototype.onWidgetChanged;
        nodeType.prototype.onWidgetChanged = function () {
            const result = onWidgetChanged?.apply(this, arguments);

            // Extract arguments
            const widget_name = arguments[0];
            const new_val = arguments[1];
            const old_val = arguments[2];
            const widget = arguments[3];

            // Skip if not a dynamic input widget or already processing connections
            if (!isDynamicInput(widget_name) || isProcessingConnection) {
                return result;
            }

            // Find the dynamic group for this widget
            const dynamicGroup = this.getDynamicGroup(widget_name);
            if (dynamicGroup === undefined) {
                return result;
            }

            // Check if widget value changed between default and non-default
            const default_val = getWidgetDefaultValue(widget);
            const wasEmpty = old_val === default_val;
            const isNowEmpty = new_val === default_val;

            // Only process if the empty state changed
            if (wasEmpty === isNowEmpty) {
                return result;
            }

            // Prevent recursive processing
            isProcessingConnection = true;

            if (wasEmpty && !isNowEmpty) {
                // Widget changed from empty to non-empty (like connecting an input)
                handleDynamicInputActivation.call(this, dynamicGroup);
            } else if (!wasEmpty && isNowEmpty) {
                // Widget changed to empty (like disconnecting an input)
                handleEmptyDynamicInput.call(this);
            }

            isProcessingConnection = false;
            return result;
        }

        // Method to swap two inputs in the "this.inputs" array by their indices
        nodeType.prototype.swapInputs = function(indexA, indexB) {
            // Validate indices
            if (
                indexA < 0 || indexB < 0 ||
                indexA >= this.inputs.length ||
                indexB >= this.inputs.length ||
                indexA === indexB
            ) {
                console.error("Invalid input indices for swapping:", indexA, indexB);
                return;
            }

            // Handle widgets if both inputs have them
            const hasWidgetA = this.inputs[indexA].widget !== undefined;
            const hasWidgetB = this.inputs[indexB].widget !== undefined;

            if (hasWidgetA && hasWidgetB) {
                // Find widget indices
                const widgetIdxA = this.widgets.findIndex(
                    (w) => w.name === this.inputs[indexA].widget.name
                );
                const widgetIdxB = this.widgets.findIndex(
                    (w) => w.name === this.inputs[indexB].widget.name
                );

                // Swap widget positions
                [this.widgets[widgetIdxA].y, this.widgets[widgetIdxB].y] =
                    [this.widgets[widgetIdxB].y, this.widgets[widgetIdxA].y];
                [this.widgets[widgetIdxA].last_y, this.widgets[widgetIdxB].last_y] =
                    [this.widgets[widgetIdxB].last_y, this.widgets[widgetIdxA].last_y];

                // Swap the widgets themselves
                [this.widgets[widgetIdxA], this.widgets[widgetIdxB]] =
                    [this.widgets[widgetIdxB], this.widgets[widgetIdxA]];

                // Swap widget values if they exist
                if (this.widgets_values) {
                    [this.widgets_values[widgetIdxA], this.widgets_values[widgetIdxB]] =
                        [this.widgets_values[widgetIdxB], this.widgets_values[widgetIdxA]];
                }
            } else if (hasWidgetA || hasWidgetB) {
                console.error("Bad swap: one input has a widget but the other doesn't", indexA, indexB);
            }

            // Swap input properties
            [this.inputs[indexA].boundingRect, this.inputs[indexB].boundingRect] =
                [this.inputs[indexB].boundingRect, this.inputs[indexA].boundingRect];
            [this.inputs[indexA].pos, this.inputs[indexB].pos] =
                [this.inputs[indexB].pos, this.inputs[indexA].pos];

            // Swap the inputs themselves
            [this.inputs[indexA], this.inputs[indexB]] =
                [this.inputs[indexB], this.inputs[indexA]];

            // Update indices to maintain connections
            updateSlotIndices(this);

            // The calling method is responsible for redrawing the canvas if needed
        };

        // Add helper method to get dynamic slots info
        nodeType.prototype.getDynamicSlots = function(dynamicGroup = null) {
            const dynamicSlots = [];
            const dynamicGroupCount = {};
            const dynamicGroupConnected = {};

            // Process each input to gather information about dynamic inputs
            for (const [index, input] of this.inputs.entries()) {
                // Skip non-dynamic inputs
                if (!isDynamicInput(input.name)) {
                    continue;
                }

                // Get the dynamic group for this input
                const currentDynamicGroup = this.getDynamicGroup(input.name);

                // Skip if filtering by group and this doesn't match
                if (dynamicGroup !== null && currentDynamicGroup !== dynamicGroup) {
                    continue;
                }

                // Determine if this input is active (connected or has non-default widget value)
                const isActive = !isDynamicInputEmpty(this, index);

                // Initialize group tracking if this is the first input for this group
                if (!(currentDynamicGroup in dynamicGroupCount)) {
                    dynamicGroupCount[currentDynamicGroup] = 0;
                    dynamicGroupConnected[currentDynamicGroup] = [];
                }

                // Get the base name for this dynamic input
                const baseNameInfo = dynamicInputs[dynamicInputGroups[currentDynamicGroup][0]];

                // Track connection status for this input in its group
                if (input.name.startsWith(baseNameInfo.baseName)) {
                    const groupIndex = dynamicGroupCount[currentDynamicGroup];
                    // Use OR assignment to preserve 'true' values
                    dynamicGroupConnected[currentDynamicGroup][groupIndex] =
                        dynamicGroupConnected[currentDynamicGroup][groupIndex] || isActive;
                    dynamicGroupCount[currentDynamicGroup]++;
                }

                // Store detailed information about this dynamic input
                dynamicSlots.push({
                    index,
                    name: input.name,
                    isWidget: input.widget !== undefined,
                    shape: input.shape,
                    connected: isActive,
                    isDynamic: true,
                    dynamicGroup: currentDynamicGroup,
                    dynamicGroupCount: dynamicGroupCount[currentDynamicGroup]
                });
            }

            return {
                slots: dynamicSlots,
                groupCount: dynamicGroupCount,
                groupConnected: dynamicGroupConnected
            };
        };

        /**
         * Generate a new dynamic input name based on type and count.
         * @param {string} dynamic - The dynamic type ('number' or 'letter').
         * @param {string} baseName - The base name for the input.
         * @param {number} count - The count/position for the new input.
         * @returns {string} The generated input name.
         */
        const generateDynamicInputName = (dynamic, baseName, count) => {
            if (dynamic === 'letter') {
                // For letter type, use the next letter in sequence
                return String.fromCharCode(97 + count); // 97 is ASCII for 'a'
            } else {
                // For number type, use baseName + index
                return `${baseName}${count}`;
            }
        };

        // Add helper method to add new dynamic input for a group
        nodeType.prototype.addNewDynamicInputForGroup = function(dynamicGroup, lastDynamicIdx) {
            let insertPosition = lastDynamicIdx + 1;
            let inputInRange = true;

            // Add new inputs for each member of the dynamic group
            for (const groupMember of dynamicInputGroups[dynamicGroup]) {
                const dynamicInput = dynamicInputs[groupMember];
                const baseName = dynamicInput.baseName;
                const dynamicType = dynamicInput.dynamicType;
                const widgetType = dynamicInput.widgetType ?? dynamicType;
                const dynamic = dynamicInput.dynamic;

                // Get current slots for this group
                const { slots } = this.getDynamicSlots(dynamicGroup);
                const groupSlots = slots.filter(s => s.name.startsWith(baseName));

                // Check if we've reached the limit for letter inputs (a-z)
                if (dynamic === 'letter' && groupSlots.length >= 26) {
                    inputInRange = false;
                    continue;
                }

                // Generate the new input name based on current count
                const newName = generateDynamicInputName(dynamic, baseName, groupSlots.length);

                // Find a reference slot to copy properties from
                const referenceSlot = groupSlots[0] || slots.find(s =>
                    s.name.startsWith(dynamicInput.baseName)
                );

                // Create the new input at the correct position
                this.addInputAtPosition(
                    newName,
                    dynamicType,
                    widgetType,
                    insertPosition++,
                    referenceSlot?.isWidget ?? false,
                    referenceSlot?.shape
                );

                // Ensure inputs are numbered correctly
                this.renumberDynamicInputs(baseName, dynamicInputs, dynamic);
            }

            return inputInRange;
        };

        // Add method to safely renumber dynamic inputs without breaking connections
        nodeType.prototype.renumberDynamicInputs = function(baseName, dynamicInputs, dynamic) {
            // Collect information about dynamic inputs with this base name
            const dynamicInputInfo = [];

            // Find all inputs that match this base name
            for (let i = 0; i < this.inputs.length; i++) {
                const input = this.inputs[i];

                if (isDynamicInput(input.name) && input.name.startsWith(baseName)) {
                    // Store info about this input
                    dynamicInputInfo.push({
                        index: i,
                        widgetIdx: input.widget !== undefined
                            ? this.widgets.findIndex((w) => w.name === input.widget.name)
                            : undefined,
                        name: input.name,
                        connected: input.isConnected
                    });
                }
            }

            // Rename inputs in place to maintain connections
            for (let i = 0; i < dynamicInputInfo.length; i++) {
                const info = dynamicInputInfo[i];
                const input = this.inputs[info.index];
                const newName = generateDynamicInputName(dynamic, baseName, i);

                // Update widget name if this input has a widget
                if (input.widget !== undefined && info.widgetIdx !== undefined) {
                    const widget = this.widgets[info.widgetIdx];
                    widget.name = newName;
                    widget.label = newName;
                    input.widget.name = newName;
                }

                // Update the input name if it's different
                if (input.name !== newName) {
                    input.name = newName;
                    input.localized_name = newName;
                }
            }
        };
    }
});
