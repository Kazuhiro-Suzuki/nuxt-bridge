<template>
                <v-col cols="12" style="margin-bottom: 24px;">
                    <span class="section-title">{{ section.sectionLabel }}</span>
                    <v-row v-for="(field, i) in section.fields" :key="i + ':' + field.name" no-gutters><!--フォームの繰り返し-->
                        <v-col cols="11" style="margin: 12px auto 0">
                            <template v-if="[
                                    '一行テキスト',
                                    '複数行テキスト',
                                    '数値',
                                    '電話番号',
                                    'メールアドレス',
                                    'パスワード',
                                    '時間',
                                    '日付',
                                    'プルダウン選択',
                                    '選択ボタン',
                                    '二択選択',
                                    '生年月日',
                                    'ファイル',
                                ].includes(field.type)
                                ">
                                <pre><span class="field-label">{{ field.label }}</span></pre>
                                <variable-field v-model="initialValue[field.name]" :valueName="field.name" :type="field.type" :min="Number(field.min)" :max="Number(field.max)"
                                    :step="field.step" :placeholder="field.placeholder" :hint="field.hint"
                                    :maxlength="field.maxlength" :suffix="field.suffix" :required="field.required"
                                    :readonly="field.readonly" :fragments="field.fragments"
                                    :placeholders="field.placeholders" :options="field.options" :validatio="field.validatio"
                                    :multiple="field.multiple" @change="changeEvent($event, field.name)"/>
                            </template>
                            <template v-else-if="'見出し（表示のみ）' == field.type">
                                <!--ラベルの表示-->
                                <span class="title">{{ field.label }}</span>
                            </template>

                            <template v-else-if="'メッセージ（表示のみ）' == field.type">
                                <!--メッセージの表示-->
                                <h4 class="title">{{ field.label }}</h4>
                                <span v-html="field.html"></span>
                            </template>
                            <template v-else-if="'画像（表示のみ）' == field.type">
                                <!--メッセージの表示-->
                                <img :style="imgStyle(field)" :src="field.base64File" />
                            </template>
                        </v-col>
                    </v-row>
                </v-col>
</template>

<script>
import variableField from "@/components/atoms/support-file/VariableField.vue";
import { mapActions } from "vuex";
export default {
    name: "VariableForm",
    components: {
        variableField,
    },
    filters: {},
    model: {
        prop: "value",
        event: "change",
    },
    props: {
        // これにより、`value` プロパティを別の目的に使えます
        section: {
            type: Object,
            default: null,
        },
        pageIndex: {
            type: Number,
            document: null,
        },
        value: {
            type: Object,
            default: function () {
                return {
                }
            },
        },
    },
    computed: {
        initialValue: {
            get() {
                return this.value;
            },
            set(newValue) {
                this.$emit("change", newValue);
            },
        },
    },
    data() {
        return {
            sectionFluctuation: {},
            fieldNameToSectionName: {},
            test:""
        };
    },
    methods: {
        ...mapActions(["setValue", "api"]),
        changeEvent(event, key) {
            let updateFormData = {}
            updateFormData[key] = event
            this.test = event
            this.initialValue = { ...this.value, ...updateFormData }
            this.$forceUpdate()
        },
        imgStyle(field) {
            var height = "auto"
            if (!field.heightFl) {
                height = field.height + field.heightUnit
            }
            var width = "auto"
            if (!field.widthFl) {
                width = field.width + field.widthUnit
            }
            return {
                "height": height,
                "width": width
            }
        },
        viewSection(section, value) {
            if (section.type === "hide") {
                return false;
            }
            if (section.type === "conditions") {
                if (section.conditions.name in value) {
                    switch (section.conditions.operator) {
                        case 1:
                            return value[section.conditions.name] == section.conditions.value;
                        case 2:
                            return value[section.conditions.name] != section.conditions.value;
                        case 3:
                            return value[section.conditions.name] > section.conditions.value;
                        case 4:
                            return value[section.conditions.name] < section.conditions.value;
                        case 5:
                            return value[section.conditions.name] >= section.conditions.value;
                        case 6:
                            return value[section.conditions.name] <= section.conditions.value;
                    }
                }
            }
            return true;
        },
    },
};
</script>

<style scoped>
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
