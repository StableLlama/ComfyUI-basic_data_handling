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
                dynamicInputs.push({name, baseName, matcher, /*forceInput,*/ dynamic, dynamicType, dynamicGroup});
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
                //if (input.link !== null) {
                    const link = node.graph._links.get(input.link);
                    if (link) {
                        link.target_slot = index;
                    } else {
                        console.error(`Input ${index} has an invalid link.`);
                    }
                }
            });
        };


        // Override onConfigure: Ensure dynamic inputs are continuously ordered
        /*
        const onConfigure = nodeType.prototype.onConfigure;
        nodeType.prototype.onConfigure = function() {
            const result = onConfigure?.apply(this, arguments);
            let lastDynamicIdx = -1
            for (let idx = 0; idx < this.inputs.length; idx++) {
                const input = this.inputs[idx];
                const isDynamic = isDynamicInput(input.name);
                if (isDynamic) {
                    if (lastDynamicIdx < 0 || lastDynamicIdx === idx - 1) {
                        lastDynamicIdx = idx;
                    } else {
                        // non-continuous dynamic inputs -> move up
                        for (let i = idx-1; i > lastDynamicIdx; i--) {
                            this.swapInputs(i, i + 1);
                        }
                        lastDynamicIdx++;
                    }
                }
            }
            return result;
        }
         */

        // Add helper method to insert input at a specific position
        nodeType.prototype.addInputAtPosition = function (name, type, position, isWidget, shape) {
            console.warn("Adding input at position:", name, type, position, isWidget, shape, app);
            if (isWidget) {
                this.addWidget(type, name, '', ()=>{}, {});

                const GET_CONFIG = Symbol();
                const input = this.addInput(name, type, {
                    shape,
                    //widget: { name: inputName, [GET_CONFIG]: () => inputSpecV1 }
                    widget: {name, [GET_CONFIG]: () =>{}}
                  })

                //widget.dynamicPrompts = true;
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

            isProcessingConnection = true;

            try {
                // Get dynamic input slots
                const dynamicSlots = [];
                const dynamicGroupCount = [];
                const dynamicGroupConnected = [];
                for (const [index, input] of this.inputs.entries()) {
                    const isDynamic = isDynamicInput(input.name);
                    if (isDynamic) {
                        const connected = input.isConnected; //.link !== null;
                        const dynamicGroup = (() => {
                            // Find the dynamicGroup by matching the baseName with input name
                            for (const di of dynamicInputs) {
                                if (input.name.startsWith(di.baseName)) {
                                    return di.dynamicGroup;
                                }
                            }
                            return undefined;
                        })();
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
                    let foundEmtpyGroup = -1;
                    let inGroup = -1;
                    let countInGroup = 0;
                    for (let idx = 0; idx < this.inputs.length; idx++) {
                        const input = this.inputs[idx];
                        const isDynamic = isDynamicInput(input.name);
                        let hasEmptyDynamic = true;

                        if (isDynamic) {
                            for (const [i, dIG] of dynamicInputGroups.entries()) {
                                if (input.name.startsWith(dynamicInputs[dIG[0]].baseName)) {
                                    inGroup = i;
                                    break;
                                }
                            }
                            if (inGroup === -1) {
                                continue;
                            }
                            for (let i = 0; i < dynamicInputGroups[inGroup].length; i++) {
                                if (this.inputs[idx+i].name.startsWith(dynamicInputs[dynamicInputGroups[inGroup][i]].baseName)) {
                                    hasEmptyDynamic &&= this.inputs[idx+i].link === null;
                                } else {
                                    console.error("Bad dynamic group input count!");
                                    debugger;
                                }
                            }
                            if (hasEmptyDynamic) {
                                if (foundEmtpyGroup !== -1) {
                                    // only remove when we have more than one empty group
                                    for (let i = 0; i < dynamicInputGroups[inGroup].length; i++) {
                                        for (let j=0; j < this.widgets.length; j++) {
                                            if (this.widgets[j].name === this.inputs[idx].name) {
                                                this.widgets.splice(j, 1);
                                                this.widgets_values?.splice(j, 1);
                                            }
                                        }
                                        this.removeInput(idx);
                                    }
                                } else {
                                    foundEmtpyGroup = idx;
                                }
                            } else {
                                if (foundEmtpyGroup !== -1) {
                                    for (let i = 0; i < dynamicInputGroups[inGroup].length; i++) {
                                        this.swapInputs(foundEmtpyGroup + i, idx + i);
                                    }
                                    foundEmtpyGroup = idx;
                                }
                            }
                            inGroup = -1;
                        }
                    }
                    for (const groupMember of dynamicInputGroups[dynamicInputs[0].dynamicGroup]) {
                        const baseName = dynamicInputs[groupMember].baseName;
                        this.renumberDynamicInputs(baseName, dynamicInputs, dynamicInputs[0].dynamic);
                    }
                }

                this.setDirtyCanvas(true, true);
                //this.arrange();
            } catch (e) {
                console.error(e);
                debugger;
                alert(e);
            } finally {
                isProcessingConnection = false;
            }

            return result;
        };

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
                        connected: input.isConnected // .link !== null
                    });
                }
            }

            // Just rename the inputs in place - don't remove/add to keep connections intact
            for (let i = 0; i < dynamicInputInfo.length; i++) {
                const info = dynamicInputInfo[i];
                const input = this.inputs[info.index];
                const newName = dynamic === "number" ? `${baseName}${i}` : String.fromCharCode(97 + i); // 97 is ASCII for 'a'

                if (input.widget !== undefined) {
                    const widgetIdx = info.widgetIdx; // this.widgets.findIndex((w) => w.name === input.widget.name);
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
