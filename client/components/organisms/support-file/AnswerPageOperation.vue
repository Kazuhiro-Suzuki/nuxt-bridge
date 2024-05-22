<template>
    <div style="max-width: 720px; margin: 24px auto">
        <span class="p-title">{{ questionnaireForm.pages[pageIndex].pageLabel }}</span>
        <slot></slot>
        <v-row class="mt-8">
            <v-btn @click="validate()"> バリデーションチェック </v-btn>
            <v-col cols="12" v-if="nextButtonFl()" style="text-align: center">
                <v-btn class="next-btn" @click="next()"> 次へ </v-btn>
            </v-col>
            <v-col
                cols="12"
                v-if="!nextButtonFl() && !isPreview"
                style="text-align: center"
            >
                <v-btn class="next-btn" @click="send()"> 送信する </v-btn>
            </v-col>
            <v-col cols="12" v-if="pageIndex" style="text-align: center">
                <v-btn class="back-btn" @click="back()"> 戻る </v-btn>
            </v-col>
        </v-row>
    </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from "vuex";
export default {
    name: "AnswerPageOperation",
    components: {
    },
    computed: {
        ...mapState({
            pageIndex: state => state.answer.pageIndex
        }),
        ...mapGetters([
            'pageLength',
            'questionnaireForm',
        ]),
    },
    mounted() {
    },
    props: {
        isPreview: {
            type: Boolean,
            default: false,
        }
    },
    methods: {
        ...mapActions(["validate","next","back","send"]),
        nextButtonFl() {
            if (this.pageLength === undefined) {
                return false;
            } else if (this.pageLength === 1) {
                return false;
            } else {
                return this.pageIndex + 1 != this.pageLength
            }
        }
    },
};
</script>