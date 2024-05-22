<template>
    <div class="variable-type-section">
        <template v-if="type == 'fluctuation'">
            <template v-for="sectionFluctuationIndex in Number(fluctuationCount)">
                <v-btn class="delete-btn" v-if="fluctuationCount-1" @click="fluctuationDelete(sectionFluctuationIndex)" :key="'VariableTypeSelection' + sectionFluctuationIndex">
                    削除
                </v-btn>
                <VariableSection 
                    class="section"
                    :value="initialValue[sectionFluctuationIndex]" 
                    :section="section" 
                    :key="sectionFluctuationIndex" 
                    @change="initialValueUpdate(sectionFluctuationIndex, $event)"
                    />
            </template>
            <v-btn class="append-btn" variant="text" v-if="fluctuation.max > fluctuationCount" @click="fluctuationCount++">
                {{ fluctuation.buttonName }}
            </v-btn>
        </template>
        <template v-else-if="type == 'display'">
            <VariableSection v-model="initialAnswer" :section="section" />
        </template>
        <template v-else-if="type == 'conditions' && viewSection(section)">
            <VariableSection v-model="initialAnswer" :section="section" />
        </template>
        <v-divider class="mt-5" />
    </div>
</template>

<script>
import VariableSection from "@/components/molecules/support-file/VariableSection.vue"
export default {
    name: "VariableForm",
    components: {
        VariableSection,
    },
    filters: {},
    model: {
        prop: "answer",
        event: "change",
    },
    props: {
        // これにより、`value` プロパティを別の目的に使えます
        type: {
            type: String,
            default: null,
        },
        fluctuation: {
            type: Object,
            default: function () {
                return {
                    max: 2,
                    min: 1
                }
            },
        },
        section: {
           type: Object,
            default: function () {
                return {
                }
            },
        },
        answer: {
            type: Object,
            default: function () {
                return {
                }
            },
        }
    },
    wetch: {
        "fluctuation.min": function () {
            this.fluctuationCount = this.fluctuation.min
        },
        immediate: true
    },
    computed: {
        initialAnswer: {
            get() {
                return this.answer
            },
            set(answer) {
                this.$emit("change", answer);
            }
        },
        initialValue: {
            get() {
                var nameList = this.section.fields.map((x) => x.name)
                var answerList = Object.keys(this.initialAnswer).reduce((previousValue, currentValue) => {
                    if (nameList.includes(currentValue)) {
                        previousValue[currentValue] = this.initialAnswer[currentValue]
                    }
                    return previousValue
                },{});
                var tmp = {}
                Object.keys(answerList).forEach(x => {
                    if (answerList[x] !== null && typeof answerList[x] === 'object') {
                        tmp[x] = answerList[x]
                    }
                });
                return this.repeatingFormArray(tmp)
            },
            set(answer) {
                this.initialAnswer = this.repeatingFormArray(answer)
            }
        }
    },
    data() {
        return {
            fluctuationCount: 0,
        };
    },
    mounted() {
        this.fluctuationCount = Math.max(
            this.fluctuation.min,
            Object.keys(this.initialValue).length)
    },
    methods: {
        fluctuationDelete(sectionFluctuationIndex) {//削除ボタン
            for (var index in this.initialValue) {
                var keyList = Object.keys(this.initialValue)
                if (index >= sectionFluctuationIndex) {
                    this.$set(this.initialValue, keyList[Number(index-1)], this.initialValue[keyList[Number(index)]])
                }
            }
            this.fluctuationCount--
            this.initialValue = this.initialValue
            this.$set(this,"initialAnswer", this.initialValue)
        },
        repeatingFormArray(value) {//{"<index>":{"<formID>":"<data>"}....}を{"<formID>":{"<index>":"<data>"....}に変換する
            const hasProperty = (obj, key) => {
                return !!(obj) && Object.prototype.hasOwnProperty.call(obj, key);
            }
            // 結果を格納するオブジェクト
            let tempAnswer = {}
            // 入力オブジェクトのプロパティを処理
            for (const key in value) {
                if (hasProperty(value,key)) {
                    const obj = value[key];
                    // 各プロパティを処理
                    for (const prop in obj) {
                        
                        if (hasProperty(obj,prop)) {
                            if (!tempAnswer[prop]) {
                                tempAnswer[prop] = {};
                            }
                            tempAnswer[prop][key] = obj[prop];
                        }
                    }
                }
            }
            return tempAnswer
        },
        viewSection(section) {
            if (section.conditions.name in this.initialAnswer) {
                switch (section.conditions.operator) {
                    case 1:
                        return this.initialAnswer[section.conditions.name] == section.conditions.value;
                    case 2:
                        return this.initialAnswer[section.conditions.name] != section.conditions.value;
                    case 3:
                        return this.initialAnswer[section.conditions.name] > section.conditions.value;
                    case 4:
                        return this.initialAnswer[section.conditions.name] < section.conditions.value;
                    case 5:
                        return this.initialAnswer[section.conditions.name] >= section.conditions.value;
                    case 6:
                        return this.initialAnswer[section.conditions.name] <= section.conditions.value;
                }
            }
            return false
        },
        initialValueUpdate(key, event) {
            this.initialValue[key] = event
            this.initialValue = JSON.parse(JSON.stringify(this.initialValue))
        }
    },
};
</script>
<style scoped>
.variable-type-section{
    width: 100%;
    text-align: right;
}
.variable-type-section *{
    text-align: left;
}
.delete-btn{
    color: #118C46;
    background-color: #ffffff00 !important;
    box-shadow: none;
}
.delete-btn:hover + .section{
    animation: bg-color 1.5s infinite;
    border-radius: 30px;
}

@keyframes bg-color {
  0% { background-color: #faf5f0; }
  50% { background-color: #f7ece1; }
  100% { background-color: #faf5f0; }
}

.append-btn {
    color: #118C46;
    background-color: #ffffff00 !important;
    box-shadow: none;
    font-weight: bold;
    margin: 0;
    margin-right: 100%;
}
.description {
    display: block;
    color: #8a8a8a;
}

.section-title {
    text-align: left;
    font: normal normal normal 16px/24px Hiragino Sans;
    letter-spacing: 0px;
    color: #212121;
    opacity: 1;
    font-weight: 300;
}

.field-label {
    text-align: left;
    font: normal normal normal 16px/24px Hiragino Sans;
    letter-spacing: 0px;
    color: #212121;
    opacity: 1;
    font-weight: 600;
    white-space: normal;
}
</style>
