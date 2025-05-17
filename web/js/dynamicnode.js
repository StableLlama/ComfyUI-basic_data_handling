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

        const dynamicInputs = [];
        for (const name in nodeData?.input?.required ?? {}) {
            const dynamic = nodeData.input.required[name][1]?._dynamic;

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
                dynamicInputs.push({name, baseName, matcher, dynamic});
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
         * @param {Array} inputs - List of inputs for the node.
         * @param {Object} graph - Graph containing the node.
         */
        const updateSlotIndices = (inputs, graph) => {
            inputs.forEach((input, index) => {
                input.slot_index = index;
                if (input.link !== null) {
                    const link = graph._links.get(input.link);
                    if (link)
                        link.target_slot = index;
                    else
                        console.error(`Input ${index} has an invalid link.`);
                }
            });
        };


        // Override onConfigure: Ensure dynamic inputs are continuously ordered
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

        // Add helper method to insert input at a specific position
        nodeType.prototype.addInputAtPosition = function (name, type, position) {
            this.addInput(name, type); // Add new input
            const newInput = this.inputs.pop(); // Fetch the newly added input (last item)
            this.inputs.splice(position, 0, newInput); // Place it at the desired position
            updateSlotIndices(this.inputs, this.graph); // Update indices
            return newInput;
        };

        // flag to prevent loops. It is ok to be "global" as the code is not
        // running in parallel.
        let isProcessingConnection = false;

        // Override onConnectionsChange: Handle connections for dynamic inputs
        const onConnectionsChange = nodeType.prototype.onConnectionsChange;
        nodeType.prototype.onConnectionsChange = function (type, slotIndex, isConnected, link, ioSlot) {
            const result = onConnectionsChange?.apply(this, arguments);

            if (type !== TypeSlot.Input || isProcessingConnection) {
                return result;
            }

            isProcessingConnection = true;

            try {
                const baseName = dynamicInputs[0].baseName;
                const dynamicType = nodeData.input.required[dynamicInputs[0].name][0];

                // Get dynamic input slots
                const dynamicSlots = this.inputs
                    .map((input, idx) => ({
                        index: idx,
                        name: input.name,
                        connected: input.link !== null,
                        isDynamic: isDynamicInput(input.name),
                    }))
                    .filter((input) => input.isDynamic);

                // Handle connection event
                if (isConnected === TypeSlotEvent.Connect) {
                    const hasEmptyDynamic = dynamicSlots.some(di => !di.connected);

                    if (!hasEmptyDynamic) {
                        // No empty slot - add a new one after the last dynamic input
                        const lastDynamicIdx = Math.max(...dynamicSlots.map((slot) => slot.index), -1);
                        const insertPosition = lastDynamicIdx + 1;
                        let inputInRange = true;

                        let newName;
                        if (dynamicInputs[0].dynamic === 'letter') {
                            if (dynamicSlots.length > 26) {
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
                            this.addInputAtPosition(newName, dynamicType, insertPosition);

                            // Renumber inputs after addition
                            this.renumberDynamicInputs(baseName, dynamicInputs, dynamicInputs[0].dynamic);
                        }
                    }
                } else if (isConnected === TypeSlotEvent.Disconnect) {
                    let hasEmptyDynamic = false;
                    for (let idx = 0; idx < this.inputs.length; idx++) {
                        const input = this.inputs[idx];
                        const isDynamic = dynamicInputs.some(di => di.matcher.test(input.name));
                        if (hasEmptyDynamic && isDynamic) {
                            if (input.link === null) {
                                // last input is empty and this input is empty
                                this.removeInput(idx);
                                // continue with this ixd as it is now pointing to
                                // a new input
                                idx--;
                                continue;
                            }
                            // this input is dynamic and connected
                            this.swapInputs(idx, idx - 1);
                            continue;
                        }
                        if (isDynamic && input.link === null) {
                            hasEmptyDynamic = true;
                        }
                    }
                    this.renumberDynamicInputs(baseName, dynamicInputs, dynamicInputs[0].dynamic);
                }

                this.setDirtyCanvas(true, true);
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
                console.warn("Invalid input indices for swapping:", indexA, indexB);
                return;
            }

            // Swap the inputs in the array
            [this.inputs[indexA], this.inputs[indexB]] = [this.inputs[indexB], this.inputs[indexA]];
            updateSlotIndices(this.inputs, this.graph); // Refresh indices

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
                const isDynamic = dynamicInputs.some(di => di.matcher.test(input.name));

                if (isDynamic) {
                    dynamicInputInfo.push({
                        index: i,
                        name: input.name,
                        connected: input.link !== null
                    });
                }
            }

            // Sort connected first, then by index
            dynamicInputInfo.sort((a, b) => {
                if (a.connected !== b.connected) {
                    return b.connected ? 1 : -1; // Connected first
                }
                return a.index - b.index; // Keep order for same connection status
            });

            this.properties.dynamicInputs = dynamicInputInfo.length;

            // Just rename the inputs in place - don't remove/add to keep connections intact
            for (let i = 0; i < dynamicInputInfo.length; i++) {
                const info = dynamicInputInfo[i];
                const newName = dynamic === "number" ? `${baseName}${i}` : String.fromCharCode(97 + i); // 97 is ASCII for 'a'

                if (this.inputs[info.index].name !== newName) {
                    this.inputs[info.index].name = newName;
                    this.inputs[info.index].localized_name = newName;
                }
            }
        };
    }
});
