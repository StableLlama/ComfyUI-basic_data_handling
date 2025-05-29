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
            //const forceInput = combinedInputData[name][1]?.forceInput;
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
                dynamicInputs.push({name, baseName, matcher, dynamic, dynamicType, dynamicGroup});
            }
        }
        if (dynamicInputs.length === 0) {
            return;
        }

        /**
         * Utility: Check if an input is dynamic.
         * @param {string} inputName - Name of the input to check.
         */
        const isDynamicInput = (inputName) =>
            dynamicInputs.some((di) => di.matcher.test(inputName));

        /**
         * Utility: Update inputs' slot indices after reordering.
         * @param {ComfyNode} node - The node to update.
         */
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


        // Add helper method to insert input at a specific position
        nodeType.prototype.addInputAtPosition = function (name, type, position, isWidget, shape) {
            if (isWidget) {
                this.addWidget(type, name, '', ()=>{}, {});

                const GET_CONFIG = Symbol();
                const input = this.addInput(name, type, {
                    shape,
                    widget: {name, [GET_CONFIG]: () =>{}}
                  })
            } else {
                this.addInput(name, type, {shape}); // Add new input
            }
            const newInput = this.inputs.pop(); // Fetch the newly added input (last item)
            this.inputs.splice(position, 0, newInput); // Place it at the desired position
            updateSlotIndices(this); // Update indices
            return newInput;
        };

        // flag to prevent loops. It is ok to be "global" as the code is not
        // running in parallel.
        let isProcessingConnection = false;

        // Override onConnectionsChange: Handle connections for dynamic inputs
        const onConnectionsChange = nodeType.prototype.onConnectionsChange;
        nodeType.prototype.onConnectionsChange = function (type, slotIndex, isConnected, link, ioSlot) {
            const result = onConnectionsChange?.apply(this, arguments);

            if (type !== TypeSlot.Input || isProcessingConnection || !isDynamicInput(this.inputs[slotIndex].name)) {
                return result;
            }

            function getDynamicGroup(inputName) {
                // Find the dynamicGroup by matching the baseName with input name
                for (const di of dynamicInputs) {
                    if (inputName.startsWith(di.baseName)) {
                        return di.dynamicGroup;
                    }
                }
                return undefined;
            }

            isProcessingConnection = true;

            try {
                // Get dynamic input slots
                const dynamicSlots = [];
                const dynamicGroupCount = [];
                const dynamicGroupConnected = [];
                for (const [index, input] of this.inputs.entries()) {
                    const isDynamic = isDynamicInput(input.name);
                    if (isDynamic) {
                        const connected = input.isConnected;
                        const dynamicGroup = getDynamicGroup(input.name);
                        if (dynamicGroup in dynamicGroupCount) {
                            if (input.name.startsWith(dynamicInputs[dynamicInputGroups[dynamicGroup][0]].baseName)) {
                                dynamicGroupConnected[dynamicGroup][dynamicGroupCount[dynamicGroup]] ||= connected;
                                dynamicGroupCount[dynamicGroup]++;
                            }
                        } else {
                            dynamicGroupCount[dynamicGroup] = 1;
                            dynamicGroupConnected[dynamicGroup] = [connected];
                        }
                        dynamicSlots.push({
                            index,
                            name: input.name,
                            isWidget: input.widget !== undefined,
                            shape: input.shape,
                            connected,
                            isDynamic,
                            dynamicGroup,
                            dynamicGroupCount: dynamicGroupCount[dynamicGroup]
                        });

                        // sanity check to make sure every widget is in reality a widget. When loading a workflow this
                        // isn't the case so we must fix it ourselves.
                        if (this.widgets && !this.widgets.some((w) => w.name === input.name)) {
                            this.addWidget(input.type, input.name, '', ()=>{}, {});
                        }
                     }
                 }

                // Handle connection event
                if (isConnected === TypeSlotEvent.Connect) {
                    const hasEmptyDynamic = dynamicGroupConnected[0].some(dgc => !dgc);

                    if (!hasEmptyDynamic) {
                        // No empty slot - add a new one after the last dynamic input
                        const lastDynamicIdx = Math.max(...dynamicSlots.map((slot) => slot.index), -1);
                        let insertPosition = lastDynamicIdx + 1;
                        let inputInRange = true;

                        for (const groupMember of dynamicInputGroups[dynamicInputs[0].dynamicGroup]) {
                            const baseName = dynamicInputs[groupMember].baseName;
                            const dynamicType = dynamicInputs[groupMember].dynamicType;
                            let newName;
                            if (dynamicInputs[0].dynamic === 'letter') {
                                if (dynamicSlots.length >= 26) {
                                    inputInRange = false;
                                }
                                // For letter type, use the next letter in sequence
                                newName = String.fromCharCode(97 + dynamicSlots.length); // 97 is ASCII for 'a'
                            } else {
                                // For number type, use baseName + index as before
                                newName = `${baseName}${dynamicSlots.length}`;
                            }

                            if (inputInRange) {
                                // Insert the new empty input at the correct position
                                this.addInputAtPosition(newName, dynamicType, insertPosition++, dynamicSlots[groupMember].isWidget, dynamicSlots[groupMember].shape);
                                // Renumber inputs after addition
                                this.renumberDynamicInputs(baseName, dynamicInputs, dynamicInputs[0].dynamic);
                            }
                        }
                    }
                } else if (isConnected === TypeSlotEvent.Disconnect) {
                    let foundEmptyIndex = -1;

                    for (let idx = 0; idx < this.inputs.length; idx++) {
                        const input = this.inputs[idx];

                        if (!isDynamicInput(input.name)) {
                            continue;
                        }

                        if (!input.isConnected) { // Check if the input is empty
                            // remove empty input - but only when it's not the last one
                            const dynamicGroup = getDynamicGroup(input.name);
                            let isLast = true;
                            for (let i = idx + 1; i < this.inputs.length; i++) {
                                isLast &&= !this.inputs[i].name.startsWith(dynamicInputs[dynamicInputGroups[dynamicGroup][0]].baseName);
                            }
                            if (isLast) {
                                continue;
                            }

                            for (let i = idx + 1; i < this.inputs.length; i++) {
                                this.swapInputs(i - 1, i);
                            }
                            const lastIdx = this.inputs.length - 1;
                            if (this.inputs[lastIdx].widget !== undefined) {
                                const widgetIdx = this.widgets.findIndex((w) => w.name === this.inputs[lastIdx].widget.name)
                                this.widgets.splice(widgetIdx, 1);
                                this.widgets_values?.splice(widgetIdx, 1);
                            }
                            this.removeInput(lastIdx);
                        }
                    }

                    // Renumber dynamic inputs to ensure proper ordering
                    for (const groupMember of dynamicInputGroups[dynamicInputs[0].dynamicGroup]) {
                        const baseName = dynamicInputs[groupMember].baseName;
                        this.renumberDynamicInputs(baseName, dynamicInputs, dynamicInputs[0].dynamic);
                    }

                }

                this.setDirtyCanvas(true, true);
            } catch (e) {
                console.error(e);
                debugger;
                alert(e);
            } finally {
                isProcessingConnection = false;
            }

            this.graph.links.forEach(l=>console.log(`post ${l.id}: ${l.origin_id}:${l.origin_slot} -> ${l.target_id}:${l.target_slot}`,l));Object.entries(this.graph._nodes_by_id).forEach(n=>console.log(n[0],n[1].title))
            return result;
        };

        const onConnectInput = nodeType.prototype.onConnectInput;
        nodeType.prototype.onConnectInput = function(inputIndex, outputType, outputSlot, outputNode, outputIndex) {
            const result = onRemoved?.apply(this, arguments) ?? true;

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

            // reflect the swap with the widgets
            if (this.inputs[indexA].widget !== undefined) {
                if (this.inputs[indexB].widget === undefined) {
                    console.error("Bad swap: input A is a widget but input B is not", indexA, indexB);
                }
                const widgetIdxA = this.widgets.findIndex((w) => w.name === this.inputs[indexA].widget.name);
                const widgetIdxB = this.widgets.findIndex((w) => w.name === this.inputs[indexB].widget.name);
                [this.widgets[widgetIdxA].y, this.widgets[widgetIdxB].y] = [this.widgets[widgetIdxB].y, this.widgets[widgetIdxA].y];
                [this.widgets[widgetIdxA].last_y, this.widgets[widgetIdxB].last_y] = [this.widgets[widgetIdxB].last_y, this.widgets[widgetIdxA].last_y];
                [this.widgets[widgetIdxA], this.widgets[widgetIdxB]] = [this.widgets[widgetIdxB], this.widgets[widgetIdxA]];
                if (this.widgets_values) {
                    [this.widgets_values[widgetIdxA], this.widgets_values[widgetIdxB]] = [this.widgets_values[widgetIdxB], this.widgets_values[widgetIdxA]];
                }
            }

            // Swap the inputs in the array
            [this.inputs[indexA].boundingRect, this.inputs[indexB].boundingRect] = [this.inputs[indexB].boundingRect, this.inputs[indexA].boundingRect];
            [this.inputs[indexA].pos, this.inputs[indexB].pos] = [this.inputs[indexB].pos, this.inputs[indexA].pos];
            [this.inputs[indexA], this.inputs[indexB]] = [this.inputs[indexB], this.inputs[indexA]];
            updateSlotIndices(this); // Refresh indices

            // Redraw the node to ensure the graph updates properly
            // -> not needed as the calling method must do it!
            this.setDirtyCanvas(true, true);
        };

        // Add method to safely renumber dynamic inputs without breaking connections
        nodeType.prototype.renumberDynamicInputs = function(baseName, dynamicInputs, dynamic) {
            // Get current dynamic inputs info
            const dynamicInputInfo = [];

            for (let i = 0; i < this.inputs.length; i++) {
                const input = this.inputs[i];
                const isDynamic = isDynamicInput(input.name);

                if (isDynamic && input.name.startsWith(baseName)) {
                    dynamicInputInfo.push({
                        index: i,
                        widgetIdx: input.widget !== undefined ? this.widgets.findIndex((w) => w.name === input.widget.name) : undefined,
                        name: input.name,
                        connected: input.isConnected
                    });
                }
            }

            // Just rename the inputs in place - don't remove/add to keep connections intact
            for (let i = 0; i < dynamicInputInfo.length; i++) {
                const info = dynamicInputInfo[i];
                const input = this.inputs[info.index];
                const newName = dynamic === "number" ? `${baseName}${i}` : String.fromCharCode(97 + i); // 97 is ASCII for 'a'

                if (input.widget !== undefined) {
                    const widgetIdx = info.widgetIdx;
                    input.widget.name = newName;
                    this.widgets[widgetIdx].name = newName;
                    this.widgets[widgetIdx].label = newName;
                }

                if (input.name !== newName) {
                    input.name = newName;
                    input.localized_name = newName;
                }
            }
        };
    }
});
