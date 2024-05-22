<template>
    <div class="body" style="max-width: 720px; margin: 24px auto">
        <h2>{{ title }}</h2>
        <variableForm
            :repl="repl"
            :sections="sections"
            @change="change"
            />
        <div class="navigation">
            <v-btn class="back" block @click="back()">戻る</v-btn>
            <v-btn class="save" block @click="save">保存</v-btn>
        </div>
        <v-dialog
        v-model="dialog"
        width="350px"
        >
            <v-card
                prepend-icon="mdi-update"
            >
                <v-card-title>注意</v-card-title>
                <v-card-text>
                    保存していない変更は破棄されます。
                </v-card-text>
                <v-card-actions>
                    <v-btn class="back" @click="$router.back()">破棄</v-btn>
                    <v-btn class="save" @click="saveAndBack()">保存して目次へ戻る</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
import variableForm from "@/components/organisms/support-file/VariableForm.vue";
export default {
    name: "repl",
    components: {
        variableForm
    },
    computed: {
    },
    mounted() {
        this.$router.beforeEach((to, from, next) => {
            //console.log("-----")
            //next(false);
            //window.history.back();
            //next(false);
            next()
        });

    },
    props: {
    },
    async created() {
        this.supportFileRegion = await this.$axios.$get(
            `/api/v1/app/support_file/?city_code=` + this.citycode
        );
        try {
            this.supportFileRepl = await this.$axios.$get(
                `/api/v1/app/support_file/repl/id/?reol_id=` +
                this.replId
            );
            this.repl = this.supportFileRepl.repl
            this.replDefault = this.supportFileRepl.repl
            this.newFl = false
        } catch (e) {
            this.newFl = true
        }
        this.title = this.supportFileRegion[0].file.item.find(x => x.formId === this.formId).name
        this.sections = this.supportFileRegion[0].file.item.find(x => x.formId === this.formId).form
    },
    methods: {
        saveAndBack() {
            this.save()
            this.$router.back()
        },
        back() {
            if (this.changeFl) {
                this.dialog = true
            } else {
                this.$router.back()
            }
        },
        change(event) {
            this.changeFl = true
            this.$set(this, "repl", event)
            this.$forceUpdate()
        },
        async save() {
            try {
                for (const key in this.repl) {
                    const file = this.repl[key];
                    if (file instanceof File) {
                        const formData = new FormData();
                        formData.append("file", file);
                        formData.append("form_id", this.formId);
                        formData.append("form_name", key);

                        const headers = { "content-type": formData.type };
                        const res = await this.$axios.$post(
                            `/api/v1/app/support_file/img/`,
                            formData,
                            { headers }
                        );
                        this.repl[key] = res[0]
                    }
                }       
                if (this.newFl) {
                    await this.$axios.$post(`/api/v1/app/support_file/repl/?city_code=` +
                        this.citycode +
                        "&form_id=" +
                        this.formId
                        , this.repl);
                        this.changeFl=false
                } else {
                    await this.$axios.$put(`/api/v1/app/support_file/repl/?city_code=` +
                        this.citycode +
                        "&id=" +
                        this.replId
                        , this.repl);
                }
                this.$notifier.showMessage({
                    content: "保存しました。",
                    color: "info",
                });
                this.changeFl=false
            } catch (e) {
                console.log(e)
            }
        }
    },
    data() {
        return {
            formId: this.$route.query.form_id,
            replId: this.$route.query.repl_id,
            citycode: this.$route.query.citycode,
            supportFileRegion: [],
            sections: [],
            repl: {},
            changeFl: false,
            supportFileRepl: {
                length:0
            },
            newFl: true,
            title: "",
            dialog: false
        }
    }
};
</script>
<style lang="scss">
.v-main {
  background-color: #faf5f0;
}
form {
    .v-input__slot{
    background-color: #fff !important;
    }
}
.body {
  .save {
    padding: 14px 16px;
    justify-content: center;
    align-items: center;
    gap: 8px;
    max-width: 600px;
    border-radius: 12px;
    background: #118c46 !important;
    color: #fff;
    text-align: center;
    font-family: "Hiragino Kaku Gothic ProN";
    font-size: 12px;
    font-style: normal;
    font-weight: 600;
    line-height: normal;
  }
  .back {
    border: 1px solid #118C46;
    padding: 14px 16px;
    justify-content: center;
    align-items: center;
    gap: 8px;
    max-width: 600px;
    border-radius: 12px;
    background: #fff !important;
    color: #118C46;
    text-align: center;
    font-family: "Hiragino Kaku Gothic ProN";
    font-size: 12px;
    font-style: normal;
    font-weight: 600;
    line-height: normal;
  }
  .navigation {
    margin: 20px 0;
    .v-btn {
        margin: 10px;
    }
  }
}
h2:before {
    background-color: #118C46; /* 線色 */
    border-radius: 5px; /* 線幅の半分 */
    content: "";
    display: inline-block;
    height: 25px; /* 線の長さ */
    margin-right: 10px; /* 線右の余白 */
    vertical-align: middle;
    width: 10px; /* 線幅 */
}
h2{
    font-size: 25px;
    margin: 20px;
}
</style>