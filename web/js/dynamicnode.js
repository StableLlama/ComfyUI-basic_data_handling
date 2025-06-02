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

// Helper for escaping strings to be used in RegExp
const escapeRegExp = (string) => {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // $& means the whole matched string
};


app.registerExtension({
    name: 'Basic data handling: dynamic input',
    async beforeRegisterNodeDef(nodeType, nodeData, appInstance) {
        if (!nodeType.comfyClass.startsWith('Basic data handling:')) {
            return;
        }

        const combinedInputData = {
            ...(nodeData?.input?.required ?? {}),
            ...(nodeData?.input?.optional ?? {})
        };

        let combinedInputDataOrder = [];
        if (nodeData.input_order) {
            if (nodeData.input_order.required) combinedInputDataOrder.push(...nodeData.input_order.required);
            if (nodeData.input_order.optional) combinedInputDataOrder.push(...nodeData.input_order.optional);
        } else if (nodeData.input) {
            if (nodeData.input.required) combinedInputDataOrder.push(...Object.keys(nodeData.input.required));
            if (nodeData.input.optional) combinedInputDataOrder.push(...Object.keys(nodeData.input.optional));
        }

        const dynamicInputs = [];
        const dynamicInputGroups = [];

        for (const name of combinedInputDataOrder) {
            if (!combinedInputData[name]) continue;

            const dynamicSetting = combinedInputData[name][1]?._dynamic;
            const dynamicGroup = combinedInputData[name][1]?._dynamicGroup ?? 0;

            if (dynamicSetting) { // Only process for inputs marked with _dynamic
                const inputOptions = combinedInputData[name][1] || {};
                const dynamicComfyType = combinedInputData[name][0];

                let isActuallyWidget = false;
                let effectiveWidgetGuiType;

                if (inputOptions.widget?.type) {
                    isActuallyWidget = true;
                    effectiveWidgetGuiType = inputOptions.widget.type;
                } else if (inputOptions.widget && typeof inputOptions.widget === 'string') {
                    isActuallyWidget = true;
                    effectiveWidgetGuiType = inputOptions.widget;
                }
                else if (inputOptions._widgetType) {
                    isActuallyWidget = true;
                    effectiveWidgetGuiType = inputOptions._widgetType;
                } else if (inputOptions.widgetType) {
                    isActuallyWidget = true;
                    effectiveWidgetGuiType = inputOptions.widgetType;
                }
                else {
                    const comfyTypeUpper = String(dynamicComfyType).toUpperCase();
                    const implicitWidgetGuiTypesMap = {
                        "STRING": "text", "INT": "number", "FLOAT": "number",
                        "NUMBER": "number", "BOOLEAN": "toggle"
                    };

                    if (implicitWidgetGuiTypesMap[comfyTypeUpper] && inputOptions.forceInput !== true && dynamicComfyType !== '*') {
                        isActuallyWidget = true;
                        effectiveWidgetGuiType = implicitWidgetGuiTypesMap[comfyTypeUpper];
                    } else if (comfyTypeUpper === "COMBO" && inputOptions.values) {
                        isActuallyWidget = true;
                        effectiveWidgetGuiType = "combo";
                    } else {
                        isActuallyWidget = false;
                        effectiveWidgetGuiType = dynamicComfyType;
                    }
                }

                let determinedBaseName;
                let suffixExtractionMatcher;

                if (dynamicSetting === 'number') {
                    const r = /^(.*?)(\d+)$/;
                    const m = name.match(r);
                    determinedBaseName = (m && m[1] !== undefined) ? m[1] : name;
                    suffixExtractionMatcher = new RegExp(`^(${escapeRegExp(determinedBaseName)})(\\d*)$`);
                } else if (dynamicSetting === 'letter') {
                    const r = /^(.*?)([a-zA-Z])$/;
                    const m = name.match(r);
                    determinedBaseName = (m && m[1] !== undefined) ? m[1] : name;
                    suffixExtractionMatcher = new RegExp(`^(${escapeRegExp(determinedBaseName)})([a-zA-Z])$`);
                } else {
                    console.warn(`[Basic Data Handling] Unknown dynamic type: ${dynamicSetting} for input ${name} on node ${nodeType.comfyClass}`);
                    continue;
                }

                if (dynamicInputGroups[dynamicGroup] === undefined) {
                    dynamicInputGroups[dynamicGroup] = [];
                }
                dynamicInputGroups[dynamicGroup].push(dynamicInputs.length);

                dynamicInputs.push({
                    name,
                    baseName: determinedBaseName,
                    matcher: suffixExtractionMatcher,
                    dynamic: dynamicSetting,
                    dynamicComfyType,
                    dynamicGroup,
                    isWidget: isActuallyWidget,
                    actualWidgetGuiType: effectiveWidgetGuiType,
                    originalOptions: inputOptions
                });
            }
        }

        if (dynamicInputs.length === 0) {
            return;
        }

        const getDynamicInputDefinition = (inputName) => {
            for (const di of dynamicInputs) {
                const m = inputName.match(di.matcher);
                if (m && m[1] === di.baseName) {
                    return { definition: di, suffix: m[2] || "" };
                }
            }
            return null;
        };

        const isDynamicInput = (inputName) => !!getDynamicInputDefinition(inputName);

        const updateSlotIndices = (node) => {
            node.inputs.forEach((input, index) => {
                input.slot_index = index;
                if (input.link !== null && input.link !== undefined) {
                    const linkInfo = node.graph.links[input.link];
                    if (linkInfo) {
                        linkInfo.target_slot = index;
                    }
                }
            });
        };

        const getWidgetDefaultValue = (widgetDef) => { // widgetDef = { type: actualWidgetGuiType, options: originalOptions }
            const type = widgetDef.type;
            const opts = widgetDef.options || {};

            switch (String(type).toLowerCase()) {
                case 'number':
                    return opts.default ?? 0;
                case 'combo':
                    return opts.default ?? (opts.values && opts.values.length > 0 ? opts.values[0] : '');
                case 'text':
                case 'string':
                    return opts.default ?? '';
                case 'toggle':
                case 'boolean':
                    return opts.default ?? false;
                default:
                    return opts.default ?? '';
            }
        };

        const isDynamicInputEmpty = (node, inputIndex) => {
            const input = node.inputs[inputIndex];
            if (input.link !== null && input.link !== undefined) return false;

            const diData = getDynamicInputDefinition(input.name);
            if (diData && diData.definition.isWidget) {
                if (input.widget && input.widget.name) {
                    const widget = node.widgets.find(w => w.name === input.widget.name);
                    if (widget) {
                        return widget.value === getWidgetDefaultValue({
                            type: diData.definition.actualWidgetGuiType,
                            options: diData.definition.originalOptions
                        });
                    } else {
                        return true;
                    }
                } else {
                    return true;
                }
            }
            return true;
        };

        const removeWidgetForInput = (node, inputIdx) => {
            if (node.inputs[inputIdx].widget && node.inputs[inputIdx].widget.name) {
                const widgetName = node.inputs[inputIdx].widget.name;
                const widgetIdx = node.widgets.findIndex((w) => w.name === widgetName);
                if (widgetIdx !== -1) {
                    node.widgets.splice(widgetIdx, 1);
                }
            }
        };

        nodeType.prototype.getDynamicGroup = function(inputName) {
            const diData = getDynamicInputDefinition(inputName);
            return diData ? diData.definition.dynamicGroup : undefined;
        };

        const addStandardWidget = function(name, widgetGuiType, defaultValue, fullConfigOptions = {}) {
            let currentVal = defaultValue;
            const widgetSpecificOpts = { ...fullConfigOptions };

            if (String(widgetGuiType).toLowerCase() === "combo") {
                if (!widgetSpecificOpts.values && Array.isArray(fullConfigOptions.default)) {
                    widgetSpecificOpts.values = fullConfigOptions.default;
                } else if (!widgetSpecificOpts.values && fullConfigOptions.options?.values) {
                    widgetSpecificOpts.values = fullConfigOptions.options.values;
                }

                if (!widgetSpecificOpts.values) {
                    widgetSpecificOpts.values = [currentVal];
                }

                if (widgetSpecificOpts.values && !widgetSpecificOpts.values.includes(currentVal) && widgetSpecificOpts.values.length > 0) {
                    currentVal = widgetSpecificOpts.values[0];
                }
            }
            return this.addWidget(widgetGuiType, name, currentVal, () => {}, widgetSpecificOpts);
        };

        nodeType.prototype.addInputAtPosition = function (name, comfyInputType, widgetGuiType, position, isWidgetFlag, shape, widgetDefaultVal, widgetConfOpts) {
            if (isWidgetFlag) {
                addStandardWidget.call(this, name, widgetGuiType, widgetDefaultVal, widgetConfOpts);
                this.addInput(name, comfyInputType, { shape, widget: { name } });
            } else {
                this.addInput(name, comfyInputType, { shape });
            }

            const newInputIndex = this.inputs.length - 1;
            if (position < newInputIndex && position < this.inputs.length -1 ) {
                const newInput = this.inputs.pop();
                this.inputs.splice(position, 0, newInput);
            }
            updateSlotIndices(this);
            return this.inputs[position];
        };

        let isProcessingConnection = false;

        const generateDynamicInputName = (dynamicBehavior, baseName, count) => {
            if (dynamicBehavior === 'letter') {
                return `${baseName}${String.fromCharCode(97 + count)}`;
            } else { // 'number'
                return `${baseName}${count}`;
            }
        };

        nodeType.prototype.renumberDynamicInputs = function(baseNameToRenumber, dynamicBehavior) {
            const inputsToRenumber = [];
            for (let i = 0; i < this.inputs.length; i++) {
                const input = this.inputs[i];
                const diData = getDynamicInputDefinition(input.name);
                if (diData && diData.definition.baseName === baseNameToRenumber && diData.definition.dynamic === dynamicBehavior) {
                    inputsToRenumber.push({
                        inputRef: input,
                        widgetName: input.widget ? input.widget.name : null
                    });
                }
            }

            for (let i = 0; i < inputsToRenumber.length; i++) {
                const { inputRef, widgetName } = inputsToRenumber[i];
                const newName = generateDynamicInputName(dynamicBehavior, baseNameToRenumber, i);

                if (inputRef.name === newName) continue;

                if (widgetName) {
                    const widget = this.widgets.find(w => w.name === widgetName);
                    if (widget) {
                        widget.name = newName;
                    }
                    if (inputRef.widget) inputRef.widget.name = newName;
                }
                inputRef.name = newName;
            }
            updateSlotIndices(this);
        };

        const handleEmptyDynamicInput = function() { // (Content largely unchanged from previous good version, ensure it uses new DI props if needed)
            let overallChangesMade = false;
            let scanAgainPass = true;

            while (scanAgainPass) {
                scanAgainPass = false;
                const dynamicGroupInfo = new Map();

                for (let i = 0; i < this.inputs.length; i++) {
                    const currentInput = this.inputs[i];
                    const diData = getDynamicInputDefinition(currentInput.name);

                    if (!diData) continue;
                    const { definition: di, suffix } = diData;
                    const group = di.dynamicGroup;

                    if (!dynamicGroupInfo.has(group)) {
                        dynamicGroupInfo.set(group, { items: new Map() });
                    }
                    const groupData = dynamicGroupInfo.get(group);
                    if (!groupData.items.has(suffix)) {
                        groupData.items.set(suffix, { inputsInfo: [], allEmpty: true });
                    }
                    const itemData = groupData.items.get(suffix);
                    itemData.inputsInfo.push({ diDefinition: di, originalInput: currentInput, originalIndex: i });
                    if (!isDynamicInputEmpty(this, i)) { // isDynamicInputEmpty uses new DI props
                        itemData.allEmpty = false;
                    }
                }

                for (const [groupId, groupData] of dynamicGroupInfo) {
                    const { items } = groupData;
                    if (items.size === 0) continue;

                    const sortedItemSuffixes = Array.from(items.keys()).sort((a, b) => {
                        const numA = parseInt(a, 10);
                        const numB = parseInt(b, 10);
                        if (!isNaN(numA) && !isNaN(numB)) return numA - numB;
                        if (a.length !== b.length) return a.length - b.length;
                        return String(a).localeCompare(String(b));
                    });

                    let activeItemCount = 0;
                    const emptyItemSuffixes = [];
                    for (const suffix of sortedItemSuffixes) {
                        if (items.get(suffix).allEmpty) {
                            emptyItemSuffixes.push(suffix);
                        } else {
                            activeItemCount++;
                        }
                    }

                    if (emptyItemSuffixes.length === 0) continue;

                    let placeholderSuffix = null;
                    if (activeItemCount === 0 && sortedItemSuffixes.length > 0) {
                        placeholderSuffix = sortedItemSuffixes[0];
                    } else if (activeItemCount > 0 && emptyItemSuffixes.length > 0) {
                        placeholderSuffix = emptyItemSuffixes[emptyItemSuffixes.length - 1];
                    }

                    const inputsToRemoveDetails = [];
                    for (const suffix of emptyItemSuffixes) {
                        if (suffix !== placeholderSuffix) {
                            const itemData = items.get(suffix);
                            for (const inputDetail of itemData.inputsInfo) {
                                inputsToRemoveDetails.push(inputDetail);
                            }
                        }
                    }

                    if (inputsToRemoveDetails.length > 0) {
                        inputsToRemoveDetails.sort((a, b) => b.originalIndex - a.originalIndex);

                        for (const { originalInput, originalIndex } of inputsToRemoveDetails) {
                            if (this.inputs[originalIndex] === originalInput) {
                                removeWidgetForInput(this, originalIndex);
                                this.removeInput(originalIndex);
                                scanAgainPass = true;
                                overallChangesMade = true;
                            } else {
                                scanAgainPass = true;
                                overallChangesMade = true;
                            }
                        }
                        if (scanAgainPass) break;
                    }
                }
                if (scanAgainPass) continue;
            }

            if (overallChangesMade) {
                const renumberedBaseNames = new Set();
                for (const groupIdx_str in dynamicInputGroups) {
                    const groupIdx = parseInt(groupIdx_str, 10);
                    if (dynamicInputGroups[groupIdx]) {
                        for (const memberIdx of dynamicInputGroups[groupIdx]) {
                            const { baseName, dynamic } = dynamicInputs[memberIdx]; // 'dynamic' here is behavior ('number'/'letter')
                            if (!renumberedBaseNames.has(baseName + dynamic)) { // Ensure unique combination
                                this.renumberDynamicInputs(baseName, dynamic);
                                renumberedBaseNames.add(baseName + dynamic);
                            }
                        }
                    }
                }
                this.setDirtyCanvas(true, true);
            }
        };

        const handleDynamicInputActivation = function(dynamicGroup) {
            const { slots: dynamicSlotsFromGetter } = this.getDynamicSlots();

            for (const slot of dynamicSlotsFromGetter) {
                if (slot.dynamicGroup === dynamicGroup && this.widgets &&
                    !this.widgets.some((w) => w.name === slot.name)) {

                    const diData = getDynamicInputDefinition(slot.name);
                    if (diData && diData.definition.isWidget) { // Use our enhanced definition
                        const originalInputDef = diData.definition;

                        addStandardWidget.call(this, slot.name,
                            originalInputDef.actualWidgetGuiType,
                            getWidgetDefaultValue({ type: originalInputDef.actualWidgetGuiType, options: originalInputDef.originalOptions }),
                            originalInputDef.originalOptions
                        );
                    }
                }
            }

            let allExistingItemsActive = true;
            const itemSuffixesInGroup = new Set();
            const groupSlots = dynamicSlotsFromGetter.filter(s => s.dynamicGroup === dynamicGroup);

            groupSlots.forEach(s => {
                const diData = getDynamicInputDefinition(s.name);
                if (diData) itemSuffixesInGroup.add(diData.suffix);
            });

            if (itemSuffixesInGroup.size === 0 && dynamicInputGroups[dynamicGroup]?.length > 0) {
                allExistingItemsActive = true;
            } else {
                let hasCompletelyEmptyItem = false;
                for (const suffix of itemSuffixesInGroup) {
                    const inputsOfThisItem = groupSlots.filter(s => {
                        const diData = getDynamicInputDefinition(s.name);
                        return diData && diData.suffix === suffix;
                    });
                    if (inputsOfThisItem.length > 0 && inputsOfThisItem.every(s => !s.connected)) { // s.connected from getDynamicSlots
                        hasCompletelyEmptyItem = true;
                        break;
                    }
                }
                allExistingItemsActive = !hasCompletelyEmptyItem;
            }


            if (allExistingItemsActive) {
                let lastDynamicIdx = -1;
                if (groupSlots.length > 0) {
                    lastDynamicIdx = Math.max(...groupSlots.map(slot => slot.index));
                } else {
                    let maxIdx = -1;
                    for(const di of dynamicInputs){ // di is a full definition object
                        if(di.dynamicGroup < dynamicGroup) {
                            for(let i=this.inputs.length-1; i>=0; --i){
                                if(this.inputs[i].name.startsWith(di.baseName)){
                                    maxIdx = Math.max(maxIdx, i);
                                    break;
                                }
                            }
                        }
                    }
                    lastDynamicIdx = (maxIdx === -1) ? (this.inputs.length -1) : maxIdx;
                }
                this.addNewDynamicInputForGroup(dynamicGroup, lastDynamicIdx);
            }

            this.setDirtyCanvas(true, true);
        };

        // --- Event Handlers (onConnectionsChange, onConnectInput, onRemoved, onWidgetChanged) ---
        const onConnectionsChange = nodeType.prototype.onConnectionsChange;
        nodeType.prototype.onConnectionsChange = function (type, slotIndex, isConnected, link, ioSlot) {
            const originalReturn = onConnectionsChange?.apply(this, arguments);
            if (type === TypeSlot.Input && slotIndex < this.inputs.length && this.inputs[slotIndex] && isDynamicInput(this.inputs[slotIndex].name)) {
                if (isProcessingConnection) return originalReturn;
                isProcessingConnection = true;
                const dynamicGroup = this.getDynamicGroup(this.inputs[slotIndex].name);
                if (dynamicGroup !== undefined) {
                    if (isConnected === TypeSlotEvent.Connect) {
                        handleDynamicInputActivation.call(this, dynamicGroup);
                    } else if (isConnected === TypeSlotEvent.Disconnect) {
                        handleEmptyDynamicInput.call(this);
                    }
                }
                isProcessingConnection = false;
            }
            return originalReturn;
        };

        const onConnectInput = nodeType.prototype.onConnectInput;
        nodeType.prototype.onConnectInput = function(inputIndex, outputType, outputSlot, outputNode, outputIndex) {
            const result = onConnectInput?.apply(this, arguments) ?? true;
            if (this.inputs[inputIndex].link !== null && this.inputs[inputIndex].link !== undefined ) {
                const pre_isProcessingConnection = isProcessingConnection;
                isProcessingConnection = true;
                this.disconnectInput(inputIndex, true);
                isProcessingConnection = pre_isProcessingConnection;
            }
            return result;
        }

        const onRemoved = nodeType.prototype.onRemoved;
        nodeType.prototype.onRemoved = function () {
            if(!isProcessingConnection){
                isProcessingConnection = true;
                for (let i = this.inputs.length - 1; i >= 0; i--) {
                    if (this.inputs[i].link !== null && this.inputs[i].link !== undefined) {
                        this.disconnectInput(i, true);
                    }
                }
                isProcessingConnection = false;
            }
            return onRemoved?.apply(this, arguments);
        }

        const onWidgetChanged = nodeType.prototype.onWidgetChanged;
        nodeType.prototype.onWidgetChanged = function (widgetName, newValue, oldValue, widgetObject) {
            const originalReturn = onWidgetChanged?.apply(this, arguments);
            if (isProcessingConnection || !isDynamicInput(widgetName)) {
                return originalReturn;
            }
            const dynamicGroup = this.getDynamicGroup(widgetName);
            if (dynamicGroup === undefined) return originalReturn;

            const diData = getDynamicInputDefinition(widgetName);
            const defaultValue = diData ? getWidgetDefaultValue({type: diData.definition.actualWidgetGuiType, options: diData.definition.originalOptions}) : getWidgetDefaultValue(widgetObject) /*fallback*/;

            const wasEffectivelyEmpty = oldValue === defaultValue;
            const isNowEffectivelyEmpty = newValue === defaultValue;

            if (wasEffectivelyEmpty === isNowEffectivelyEmpty) return originalReturn;

            isProcessingConnection = true;
            if (wasEffectivelyEmpty && !isNowEffectivelyEmpty) {
                handleDynamicInputActivation.call(this, dynamicGroup);
            } else if (!wasEffectivelyEmpty && isNowEffectivelyEmpty) {
                handleEmptyDynamicInput.call(this);
            }
            isProcessingConnection = false;
            return originalReturn;
        };

        // --- Core Dynamic Methods (swapInputs, getDynamicSlots, addNewDynamicInputForGroup) ---
        nodeType.prototype.swapInputs = function(indexA, indexB) { // (Content unchanged)
            if (indexA < 0 || indexB < 0 || indexA >= this.inputs.length || indexB >= this.inputs.length || indexA === indexB) {
                console.error("[Basic Data Handling] Invalid input indices for swapping:", indexA, indexB); return;
            }
            const hasWidgetA = this.inputs[indexA].widget !== undefined;
            const hasWidgetB = this.inputs[indexB].widget !== undefined;
            if (hasWidgetA && hasWidgetB) {
                const widgetIdxA = this.widgets.findIndex((w) => w.name === this.inputs[indexA].widget.name);
                const widgetIdxB = this.widgets.findIndex((w) => w.name === this.inputs[indexB].widget.name);
                if(widgetIdxA !== -1 && widgetIdxB !== -1) {
                    [this.widgets[widgetIdxA].y, this.widgets[widgetIdxB].y] = [this.widgets[widgetIdxB].y, this.widgets[widgetIdxA].y];
                    [this.widgets[widgetIdxA].last_y, this.widgets[widgetIdxB].last_y] = [this.widgets[widgetIdxB].last_y, this.widgets[widgetIdxA].last_y];
                    [this.widgets[widgetIdxA], this.widgets[widgetIdxB]] = [this.widgets[widgetIdxB], this.widgets[widgetIdxA]];
                    if (this.widgets_values) {
                        [this.widgets_values[widgetIdxA], this.widgets_values[widgetIdxB]] = [this.widgets_values[widgetIdxB], this.widgets_values[widgetIdxA]];
                    }
                }
            } else if (hasWidgetA || hasWidgetB) {
                console.error("[Basic Data Handling] Bad swap: one input has a widget but the other doesn't", indexA, indexB);
            }
            [this.inputs[indexA].boundingRect, this.inputs[indexB].boundingRect] = [this.inputs[indexB].boundingRect, this.inputs[indexA].boundingRect];
            [this.inputs[indexA].pos, this.inputs[indexB].pos] = [this.inputs[indexB].pos, this.inputs[indexA].pos];
            [this.inputs[indexA], this.inputs[indexB]] = [this.inputs[indexB], this.inputs[indexA]];
            updateSlotIndices(this);
        };

        nodeType.prototype.getDynamicSlots = function(filterDynamicGroup = null) { // (Content largely unchanged, relies on isDynamicInputEmpty which is updated)
            const dynamicSlotsResult = [];
            const dynamicGroupCount = {};
            const dynamicGroupConnected = {};

            const itemsState = new Map();

            for (const [index, input] of this.inputs.entries()) {
                const diData = getDynamicInputDefinition(input.name);
                if (!diData) continue;

                const { definition: di, suffix } = diData;
                const currentDynamicGroup = di.dynamicGroup;

                if (filterDynamicGroup !== null && currentDynamicGroup !== filterDynamicGroup) continue;

                if (!itemsState.has(currentDynamicGroup)) itemsState.set(currentDynamicGroup, new Map());
                const groupItems = itemsState.get(currentDynamicGroup);
                if (!groupItems.has(suffix)) groupItems.set(suffix, { isActive: false, inputCount: 0, activeInputCount: 0 });

                const itemState = groupItems.get(suffix);
                itemState.inputCount++;
                const isInputActive = !isDynamicInputEmpty(this, index); // Uses updated isDynamicInputEmpty
                if (isInputActive) itemState.activeInputCount++;

                dynamicSlotsResult.push({
                    index, name: input.name, isWidget: input.widget !== undefined, shape: input.shape,
                    connected: isInputActive,
                    isDynamic: true, dynamicGroup: currentDynamicGroup,
                });
            }

            for(const [groupId, groupItems] of itemsState) {
                dynamicGroupCount[groupId] = groupItems.size;
                dynamicGroupConnected[groupId] = [];
                const sortedSuffixes = Array.from(groupItems.keys()).sort((a,b) => {
                    const numA = parseInt(a,10); const numB = parseInt(b,10);
                    if(!isNaN(numA) && !isNaN(numB)) return numA-numB;
                    if(a.length !== b.length) return a.length - b.length;
                    return String(a).localeCompare(String(b));
                });

                for(const suffix of sortedSuffixes){
                    const item = groupItems.get(suffix);
                    dynamicGroupConnected[groupId].push(item.activeInputCount > 0);
                }
            }
            return { slots: dynamicSlotsResult, groupCount: dynamicGroupCount, groupConnected: dynamicGroupConnected };
        };

        nodeType.prototype.addNewDynamicInputForGroup = function(dynamicGroup, lastKnownInputIndexInGroup) {
            let insertPosition = lastKnownInputIndexInGroup + 1;
            let inputInRange = true;

            const groupMemberDefinitions = dynamicInputGroups[dynamicGroup].map(idx => dynamicInputs[idx]);

            const { slots: currentGroupSlots } = this.getDynamicSlots(dynamicGroup);
            const existingSuffixes = new Set();
            currentGroupSlots.forEach(s => {
                const diData = getDynamicInputDefinition(s.name);
                if(diData) existingSuffixes.add(diData.suffix);
            });

            let newItemNumericSuffix = 0;
            // Find the smallest non-negative integer not in existingSuffixes (if they are numbers)
            // or just use existingSuffixes.size if complex/letter based for simplicity (renumbering will fix)
            // For simplicity here, using size, assuming renumbering will handle actual ordering.
            // A more robust suffix generation might be needed if strict ordering before renumbering is critical.
            const isNumericSuffix = groupMemberDefinitions.length > 0 && groupMemberDefinitions[0].dynamic === 'number';
            if (isNumericSuffix) {
                while (existingSuffixes.has(String(newItemNumericSuffix))) {
                    newItemNumericSuffix++;
                }
            } else { // letter or complex
                newItemNumericSuffix = existingSuffixes.size; // This is the 'count' for letter generation
            }


            for (const diDefinition of groupMemberDefinitions) {
                // Use the new properties from diDefinition
                const { baseName, dynamic, dynamicComfyType, isWidget, actualWidgetGuiType, originalOptions } = diDefinition;

                if (dynamic === 'letter' && newItemNumericSuffix >= 26) {
                    inputInRange = false; continue;
                }
                const newName = generateDynamicInputName(dynamic, baseName, newItemNumericSuffix);

                const refSlot = currentGroupSlots.find(s => s.name.startsWith(baseName)) || currentGroupSlots[0];

                const widgetDefault = getWidgetDefaultValue({ type: actualWidgetGuiType, options: originalOptions });

                this.addInputAtPosition(
                    newName,
                    dynamicComfyType,    // ComfyUI input type (e.g., "STRING", "*")
                    actualWidgetGuiType, // GUI widget type (e.g., "text", "number", "combo")
                    insertPosition++,
                    isWidget,            // The crucial boolean
                    refSlot?.shape,
                    widgetDefault,
                    originalOptions      // Full original options for widget config
                );
            }
            return inputInRange;
        };
    }
});
