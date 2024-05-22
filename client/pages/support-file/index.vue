<template>
  <v-container justify-center align-center >
    <v-row style="max-width: 94%; margin: 0 auto">
      <v-col cols="12">
        <p class="p-title">{{ title }}</p>
        <p class="help-link">
          <a
            href="https://d3k8u7y4yskhx8.cloudfront.net/static-files/rupinasu_manual.pdf"
            target="_parent"
            class="help-link"
          >
            <v-icon>$IconHelpLine</v-icon>使い方
          </a>
        </p>
      </v-col>
      <v-col cols="12" class="toc-col">
        <v-checkbox
          label="まとめて選択"
          color="success"
          hide-details
          style="margin-bottom: 16px"
          v-model="allSelected"
          @click="allSelect"
        ></v-checkbox>
        <table class="table">
          <tr v-for="(item, index) in items" :key="item.name">
            <td style="width: 10px">
              <v-checkbox
                v-model="selected[index+1]"
                color="success"
                @change="anySelectedFalse"
              ></v-checkbox>
            </td>
            <td class="toc-td">{{ item.name }}</td>
            <td class="edit-td" @click="replPage(item, index)">
              {{ repList[index] ? '編集':'未入力' }}<v-icon color="#118C46">$IconArrowRight</v-icon>
            </td>
            <repDialog :repl="item.repl" :title="item.name" v-model="dialogFlList[index]" :formId="item.formId" :labelKey="item.labelKey"></repDialog>
          </tr>
        </table>
        <v-checkbox
          label="まとめて選択"
          color="success"
          hide-details
          v-model="allSelected"
          @click="allSelect"
        ></v-checkbox>
      </v-col>
    </v-row>
    <v-row class="dl-row">
      <v-col class="dl-col">
        <v-row no-gutters align="center" justify="center">
          <v-col cols="5">
            <div class="selected-count">{{ selectedCount }} ページ選択中</div>
            <div class="contain-cover">
              <v-checkbox
                label="表紙を含める"
                color="success"
                hide-details
                v-model="selected[0]"
              ></v-checkbox>
            </div>
          </v-col>
          <v-col cols="6">
            <v-btn
            @click="pdfDownload"
              ><v-icon color="white">$IconDownloadLine</v-icon
              >まとめてダウンロード</v-btn
            >
          </v-col>
          <v-dialog
            v-model="dialog"
            >
              <v-card
                  prepend-icon="mdi-update"
              >
                  <v-btn class="back" @click="download">ダウンロード</v-btn>
              </v-card>
          </v-dialog>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import repDialog from "@/components/organisms/support-file/ReplDialog.vue"
import { mapGetters } from "vuex";

export default {
  components: {
    repDialog,
  },
  head() {
    return {
      title: this.title,
    };
  },
  data() {
    return {
      selected: [false],
      citycode: this.$route.query.citycode,
      title: "",
      supportFileRegion: "",
      supportFileRepl: "",
      items: [],
      allSelected: false,
      selectedCount: 0,
      containCover: false,
      supportFileId: "",
      repList: [],
      dialog: false,
      dialogFlList: []
    };
  },
  computed: {
    ...mapGetters({
      regionData: "region/getRegion",
    }),
    anySelectedFalse() {
      this.allSelected = this.selected.every(x => x);
      this.countSelected();
    }
  },
  methods: {
    download() {
      window.open(this.pdfDownloadUrl.split('"')[1])
      this.dialog = false
    },
    async pdfDownload() {
      //this.pdfDownloadUrl =  '"http://localhost:3000/specific/htp/?support_file_id=f3dcbc26-b27e-4316-914f-2136a774e35f&user_id=807165a5-fd96-44e1-a731-eccf73ddb9ee&vuefile=[0,1,0,0,0,0,0,0,0,0,0]"'
      this.pdfDownloadUrl = await this.$axios.$get(
        `/api/v1/app/support_file/pdf/?support_file_id=` +
        this.supportFileId +
        (this.selected.every(x => !x)?"":"&vuefile="+ JSON.stringify(this.selected))
      );
      console.log(this.pdfDownloadUrl.split('"')[1])
      if (!window.open(this.pdfDownloadUrl.split('"')[1])) {
        console.log("失敗")
        this.dialog = true
      } else {
        console.log("成功")
      }
    },
    countSelected() {
      this.selectedCount = this.selected.filter(x => x).length
    },
    allSelect() {
      this.selected.fill(this.allSelected)
      this.countSelected();
    },
    replPage(item, index) {
      console.log(item)
      if (item.type == "form" || item.repl.length===0) {
        let query = {
          ...this.$route.query,
          "form_id": item.formId,
          "repl_id": item.repl.length === 0 ? "": item.repl["data-page"][0].id
        }
        this.$router.push({ path: 'support-file/repl', query })
      } else {
        this.$set(this.dialogFlList, index, true)
      }
    }
  },
  async created() {
    try {
      this.supportFileRegion = await this.$axios.$get(`/api/v1/app/support_file/?city_code=` + this.citycode);
      this.supportFileId = this.supportFileRegion[0].id
      this.title = this.supportFileRegion[0].file.name;
      for (const item of this.supportFileRegion[0].file.item) {
        this.selected.push(false)
        const supportFileRepl = await this.$axios.$get(
          `/api/v1/app/support_file/repl/?city_code=` +
          this.citycode +
          "&form_id=" +
          item.formId
        );
        this.repList.push(supportFileRepl.length)
        this.dialogFlList.push(false)
        this.items.push({
          name: item.name,
          selected: false,
          formId: item.formId,
          type: item.type,
          repl: supportFileRepl,
          labelKey: item.labelKey,
          dialog: false
        });
      }
    } catch (e) {
      console.log(e);
      this.$router.push(`/account?citycode=${this.citycode}`);
      this.$notifier.showMessage({
        content: "ログインが必要です。",
        color: "error",
      });
    }
  },
};
</script>

<style lang="scss">
.v-main {
  background-color: #faf5f0;
}
.p-title {
  color: var(--Gray13, #212121);
  font-family: "Hiragino Kaku Gothic ProN";
  font-size: 24px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
  margin-bottom: 0;
  float: left;
  text-align: left;
}
.help-link {
  font-family: "Hiragino Kaku Gothic Pro";
  font-size: 16px;
  font-weight: 600;
  line-height: 36px;
  letter-spacing: 0em;
  color: #118c46 !important;
  text-align: right;
  .v-icon {
    color: #118c46;
    width: 18px;
    height: 18px;
    padding-bottom: 2px;
    margin-right: 2px;
  }
}
.toc-col {
  padding-top: 0;
  .v-input--checkbox {
    .v-label {
      color: var(--Gray13, #212121);
      font-family: "Hiragino Kaku Gothic ProN";
      font-size: 16px;
      font-style: normal;
      font-weight: 300;
      line-height: normal;
    }
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
      padding: 0 18px;
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
}
.dl-row {
  justify-content: flex-end !important;
  .dl-col {
    max-width:50%;
    border-radius: 5px;
    background: white;
    border: 1px solid var(--Gray87, #dedede);
    .selected-count {
      padding-left: 7px;
      color: #000;
      font-family: "Hiragino Kaku Gothic ProN";
      font-size: 14px;
      font-style: normal;
      font-weight: 600;
      line-height: normal;
    }
    .contain-cover {
      .v-input--selection-controls {
        margin-top: 0;
      }
      .v-label {
        color: var(--Gray13, #212121);
        font-family: "Hiragino Kaku Gothic ProN";
        font-size: 14px;
        font-style: normal;
        font-weight: 300;
        line-height: normal;
      }
    }
    .v-btn {
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
  }
}
@media (max-width:760px) {
  .align-center{
    margin: 0;
  }
  .dl-row {
    justify-content:left !important;
    .dl-col {
      max-width:100%;
    }
  }
}
</style>
