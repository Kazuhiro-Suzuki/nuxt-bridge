<template>
    <v-dialog
        v-model="initialDialogFl"
        scrollable
        width="350px"
        >
        <v-card>
            <v-card-title class="title">{{ title }}</v-card-title>
            <v-divider></v-divider>
            <v-card-text style="height: 300px;">
                <table class="table">
                    <tr v-for="(x, i) in list" :key="i" @click="replPage(x.id)">
                        <td>{{ x.repl[labelKey] }}</td>
                        <td class="edit-td"><v-icon color="#118C46">$IconArrowRight</v-icon></td>
                    </tr>
                </table>
                <v-btn
                    v-if="maxPage > page"
                    :loading="loading"
                    elevation="0"
                    class="close-btn"
                    variant="text"
                    @click="load"
                >
                    読み込み
                </v-btn>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions class="footer">
                <v-btn
                    class="add-btn"
                    color="blue-darken-1"
                    variant="text"
                    elevation="0"
                    block
                    @click="replPage('')"
                >
                    +記録の追加
                </v-btn>
                <v-btn
                    elevation="0"
                    class="close-btn"
                    variant="text"
                    @click="initialDialogFl = false"
                >
                    閉じる
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>
<script>
export default {
    data() {
        return {
            citycode: this.$route.query.citycode,
            fl: true,
            page: 1,
            list: [],
            maxPage: 1,
            loading: false

        }
    },
    created() { 
        this.list = this.repl['data-page']
        this.maxPage = this.repl["max-page"]
    },
    methods: {
        replPage(replId) { 
            let query = {
                ...this.$route.query,
                "form_id": this.formId,
                "repl_id": replId
            }
            this.$router.push({ path: 'support-file/repl', query })
        },
        async load() {
            this.loading=true
            this.page++
            const supportFileRepl = await this.$axios.$get(
                `/api/v1/app/support_file/repl/?city_code=` +
                this.citycode +
                "&form_id=" +
                this.formId +
                "&page=" +
                this.page
            );
            this.list = this.list.concat(supportFileRepl['data-page'])
            this.loading=false
        }
    },
    model: {
        prop: "dialogFl",
        event: "change",
    },
    props: {
        formId: {
            type: String,
            default: "",
        },
        title: {
            type: String,
            default: "",
        },
        dialogFl: {
            type: Boolean,
            document: true,
        },
        repl: {
            type: Object,
            default: function () {
                return {}
            },
        },
        labelKey: {
            type: String,
            default: "",
        }
    },
    computed: {
        initialDialogFl: {
            get() {
                return this.dialogFl;
            },
            set(newValue) {
                this.$emit("change", newValue);
            }
        }
    }
}
</script>

<style lang="scss">
    .close-btn{
        background-color: #ffffff00 !important;
    }
    .footer{
        display: block;
        text-align: center;
    }
    .add-btn {
        border: 1px solid #118C46;
        padding: 14px 16px;
        justify-content: center;
        align-items: center;
        gap: 8px;
        max-width: 600px;
        border-radius: 12px;
        background: #ffffff !important;
        color: #118C46 !important;
        text-align: center;
        font-family: "Hiragino Kaku Gothic ProN";
        font-size: 12px;
        font-style: normal;
        font-weight: 600;
        line-height: normal;
    }
  .table {
    width: 100%;
    text-align: center;
    border-collapse: separate;
    border-spacing: 0;
    border: 1px solid var(--Gray87, #dedede);
    background: var(--White, #fff);
    border-radius: 10px;
    -webkit-border-radius: 10px;
    -moz-border-radius: 10px;
    td {
      font-size: 30px;
      padding: 5px;
      border-bottom: solid 1px #dedede;
    }
    tr:last-child td {
      border-bottom: none;
    }
    .toc-td {
      text-align: left;
      color: var(--Gray13, #212121);
      font-family: "Hiragino Kaku Gothic ProN";
      font-size: 16px;
      font-style: normal;
      font-weight: 600;
      line-height: normal;
    }
    .edit-td {
      color: var(--Gray62, #9e9e9e);
      text-align: right;
      font-family: "Hiragino Kaku Gothic ProN";
      font-size: 12px;
      font-style: normal;
      font-weight: 300;
      line-height: normal;
    }
  }
  .title:before {
    background-color: #118C46; /* 線色 */
    border-radius: 5px; /* 線幅の半分 */
    content: "";
    display: inline-block;
    height: 25px; /* 線の長さ */
    margin-right: 10px; /* 線右の余白 */
    vertical-align: middle;
    width: 10px; /* 線幅 */
}
.title{
    font-size: 25px;
}
  </style>