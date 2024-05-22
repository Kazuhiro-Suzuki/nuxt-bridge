<template>
  <div style="margin-top: 5px">
    <template v-if="['一行テキスト', '数値', 'メールアドレス'].includes(type)">
      <v-text-field
        v-model="initialValue"
        :type="getFormType(type)"
        :step="step"
        :maxlength="maxlength"
        :readonly="readonly"
        :placeholder="placeholder"
        :rules="roleSelect(type)"
        :hint="hint"
        :persistent-hint="true"
        outlined
        dense
      />
    </template>
    <template v-else-if="type === '電話番号'">
      <v-text-field
        v-model="initialValue"
        type="tel"
        :step="step"
        :maxlength="maxlength"
        :readonly="readonly"
        :placeholder="placeholder"
        :hint="hint"
        :persistent-hint="true"
        outlined
        dense
        class="phone-field"
      />
    </template>
    <template v-else-if="type === 'パスワード'">
      <v-text-field
        v-model="initialValue"
        :append-icon="isPassMask ? 'mdi-eye' : 'mdi-eye-off'"
        :type="isPassMask ? 'text' : 'password'"
        :readonly="readonly"
        :placeholder="placeholder"
        :rules="roleSelect(type)"
        :hint="hint"
        :persistent-hint="true"
        outlined
        dense
        counter
        @click:append="isPassMask = !isPassMask"
      ></v-text-field>
    </template>
    <template v-else-if="type === '時間'">
      <v-menu
        ref="menu"
        v-model="timeMenuFlg"
        :close-on-content-click="false"
        :nudge-right="40"
        transition="scale-transition"
        offset-y
        max-width="290px"
        min-width="290px"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            v-model="initialValue"
            prepend-icon="mdi-clock-time-four-outline"
            :placeholder="placeholder"
            :rules="roleSelect(type)"
            :readonly="readonly"
            v-bind="attrs"
            v-on="on"
          ></v-text-field>
        </template>
        <v-time-picker
          v-if="timeMenuFlg"
          v-model="initialValue"
          :readonly="readonly"
          outlined
          dense
          format="24hr"
        ></v-time-picker>
      </v-menu>
    </template>
    <template v-else-if="type === '日付' || type === '生年月日'">
      <v-menu
        v-model="dateMenuFlg"
        :close-on-content-click="false"
        :nudge-right="40"
        transition="scale-transition"
        offset-y
        min-width="auto"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            v-model="initialValue"
            prepend-icon="mdi-calendar"
            :placeholder="placeholder"
            :rules="roleSelect('日付')"
            readonly
            v-bind="attrs"
            v-on="on"
            outlined
            dense
          ></v-text-field>
        </template>
        <v-date-picker
          v-model="initialValue"
          @input="dateMenuFlg = false"
          :readonly="readonly"
        ></v-date-picker>
      </v-menu>
    </template>
    <template v-else-if="type === '複数行テキスト'">
      <v-textarea
        v-model="initialValue"
        :label="label"
        :placeholder="placeholder"
        :readonly="readonly"
        :rules="roleSelect(type)"
        :hint="hint"
        :persistent-hint="true"
        outlined
        dense
      />
    </template>
    <template v-else-if="type === 'プルダウン選択'">
      <v-select
        v-model="initialValue"
        :items="options.split(',')"
        outlined
        dense
        :rules="roleSelect(type)"
        :readonly="readonly"
        :placeholder="placeholder"
        :hint="hint"
        :persistent-hint="true"
        :multiple="multiple"
      />
    </template>
    <template v-else-if="type === 'checkbox'">
      <v-checkbox
        v-model="initialValue"
        v-for="option in options"
        :key="option"
        :value="option"
        :input-value="value"
        :label="option"
      />
    </template>
    <template v-else-if="type === 'radio'">
      <v-radio-group>
        <v-radio
          v-model="initialValue"
          v-for="option in options"
          :key="option"
          :label="option"
          :value="option"
        />
      </v-radio-group>
    </template>
    <template v-else-if="type === '選択ボタン'">
      <SelectionSwitchMultiple
        v-if="multiple"
        v-model="initialValue"
        :options="options.split(',')"
      ></SelectionSwitchMultiple>
      <SelectionSwitch
        v-else
        v-model="initialValue"
        :options="options.split(',')"
      />
    </template>
    <template v-else-if="type === 'yesNo'">
      <yes-no-switch
        v-model="initialValue"
        :radioName="valueName"
        yes-label="はい"
        no-label="いいえ"
      />
    </template>
    <template v-else-if="type === '二択選択'">
      <yes-no-switch
        v-model="initialValue"
        :radioName="valueName"
        yes-label="はい"
        no-label="いいえ"
      />
      <span style="color: rgba(0, 0, 0, 0.6); font-size: 12px">{{ hint }}</span>
    </template>
    <template v-else-if="type === 'tokenizedText'">
      <div class="d-flex">
        <div
          v-for="f in fragmentValues"
          :key="f.label"
          class="flex-grow-1 px-1"
        >
          <v-text-field
            v-model="initialValue"
            type="text"
            :label="f.label"
            :placeholder="f.placeholder"
            :maxlength="maxlength"
            :value="f.value"
            :readonly="readonly"
          ></v-text-field>
        </div>
      </div>
    </template>
    <template v-else-if="type === 'tokenizedNumber'">
      <div class="d-flex">
        <div
          v-for="f in fragmentValues"
          :key="f.label"
          class="flex-grow-1 px-1"
        >
          <v-text-field
            v-model="initialValue"
            type="number"
            :label="f.label"
            :placeholder="f.placeholder"
            :min="min"
            :max="max"
            :step="step"
            :value="f.value"
            :readonly="readonly"
          ></v-text-field>
        </div>
      </div>
    </template>
    <template v-else-if="type === 'ファイル'">
      <label for="img">
        <div v-if="initialValue" class="img-preview">
          <img :src="imageUrl" />
        </div>
      </label>
      <v-file-input
        v-model="initialValue"
        id="img"
        type="file"
        outlined
        @change="changeImgUrl"
      ></v-file-input>
    </template>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import YesNoSwitch from "@/components/atoms/support-file/form/YesNoSwitch.vue";
import SelectionSwitch from "@/components/atoms/support-file/form/SelectionSwitch.vue";
import SelectionSwitchMultiple from "@/components/atoms/support-file/form/SelectionSwitchMultiple.vue";

export default {
  name: "VariableField",
  components: {
    SelectionSwitch,
    YesNoSwitch,
    SelectionSwitchMultiple,
  },
  data() {
    return {
      formTypes: {
        一行テキスト: "text",
        数値: "number",
        電話番号: "number",
        メールアドレス: "text",
      },
      timeMenuFlg: false,
      dateMenuFlg: false,
      isPassMask: false,
      imageUrl: ''
    };
  },
  props: {
    type: {
      type: String,
      default: "text",
      /*
      text: 1行テキスト
      textarea: 複数行テキスト
      number, tel, email, password: 対応する標準のテキスト入力
      time, date: 対応するブラウザ標準の時刻、日付入力
      select: ドロップダウン
      radio: ラジオボタン
      checkbox: チェックボックス
      selectSwitch: ボタン表現のラジオボタン
      yesNo: はい/いいえ 選択
      presence: あり/なし 選択
      tokenizedText: 複数片に別れたテキスト入力
      tokenizedNumber: 複数片に別れた数値入力
       */
    },
    label: {
      type: String,
      default: null,
    },
    valueName: {
      type: String,
      default: null,
    },
    placeholder: {
      type: String,
      default: null,
    },
    hint: {
      type: String,
      default: null,
    },
    persistentHint: {
      type: Boolean,
      default: false,
    },
    multiple: {
      type: Boolean,
      default: false,
    },
    min: {
      type: Number,
      default: 99,
    },
    max: {
      type: Number,
      default: 99,
    },
    step: {
      type: Number,
      default: 1,
    },
    maxlength: {
      type: Number,
      default: undefined,
    },
    suffix: {
      type: String,
      default: undefined,
    },
    fragments: {
      type: Array,
      default: () => [],
    },
    placeholders: {
      type: Array,
      default: () => [],
    },
    options: {
      type: String,
      default: "",
    },
    required: {
      type: Boolean,
      default: false,
    },
    readonly: {
      type: Boolean,
      default: false,
    },
    validatio: {
      type: Array,
      default: () => [],
    },
    value: {},
  },
  model: {
    prop: "value",
    event: "change",
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
    fragmentValues() {
      const fragmentValues = [];
      // value 要素数が fragments より少ない場合を考慮すると _.zip が使えないため for で回す
      for (let i = 0; i < this.fragments.length; i++) {
        fragmentValues.push({
          label: this.fragments[i],
          value: this.value.length > i ? this.value[i] : null,
          placeholder:
            this.placeholders.length > i ? this.placeholders[i] : null,
        });
      }
      return fragmentValues;
    },
  },
  async mounted() {
    // サーバーから非同期処理で画像URLを取得
    console.log("test");
    if (this.type === "ファイル") {
      const image = await this.getImgUrl(this.value);
      this.imageUrl = image
      return { imageUrl: image };
    }
  },
  methods: {
    ...mapActions(["setValue", "api"]),
    changeImgUrl(file){
      if(file) {
        this.imageUrl = URL.createObjectURL(file);
      }
    },
    async getImgUrl(filename) {
      if (typeof filename == "string") {
        const res = this.$axios
          .$get(`/api/v1/app/support_file/img/?id=` + filename)
        return res;
      } else if (filename) {
        return URL.createObjectURL(filename);
      }
    },
    getFormType(label) {
      return this.formTypes[label];
    },
    test(x) {
      const a = /[0-5]+/;
      console.log(a.test("11")); //true
      console.log(a.test("88")); //false
      return /[0-9]+/.test(x);
    },
    roleSelect(type) {
      var additionalCheck = this.validatio.map((x) => {
        switch (x) {
          case "hiragana":
            return (v) => {
              return (
                /^[\u3040-\u309F]+$/.test(v) || "ひらがな以外は入力できません。"
              );
            };
          case "katakana":
            return (v) => {
              return (
                /^[\u30A0-\u30FF]+$/.test(v) || "カタカナ以外は入力できません。"
              );
            };
        }
      });
      return {
        一行テキスト: [
          (x) => {
            // if (!x) return true;
            if (!this.min) return true;
            return (
              (!!x && this.min <= x.length) ||
              `${this.min} 文字以上で入力してください。`
            );
          },
          (x) => {
            // if (!x) return true;
            if (!this.max) return true;
            return (
              (!!x && x.length <= this.max) ||
              `${this.max} 文字以内で入力してください。`
            );
          },
          (x) => {
            if (this.required && !x.trim()) {
              return "回答必須項目です。";
            } else {
              return true;
            }
          },
        ],
        複数行テキスト: [
          (x) => {
            if (this.required && !x.trim()) {
              return "回答必須項目です。";
            } else {
              return true;
            }
          },
          (x) => {
            // if (!x) return true;
            if (!this.min) return true;
            return (
              (!!x && this.min <= x.length) ||
              `${this.min} 文字以上で入力してください。`
            );
          },
          (x) => {
            // if (!x) return true;
            if (!this.max) return true;
            return (
              (!!x && x.length <= this.max) ||
              `${this.max} 文字以内で入力してください。`
            );
          },
        ],
        数値: [
          (x) => {
            // if (!x) return true;
            if (!this.min) return true;
            return (
              (!!x && this.min <= Number(x)) ||
              `${this.min} 以上の数値を入力してください。`
            );
          },
          (x) => {
            // if (!x) return true;
            if (!this.max) return true;
            return (
              (!!x && Number(x) <= this.max) ||
              `${this.max} 以内の数値を入力してください。`
            );
          },
          (x) => {
            if (this.required && !x.trim()) {
              return "回答必須項目です。";
            } else {
              return true;
            }
          },
        ],
        メールアドレス: [
          (x) => {
            if (this.required && !x.trim()) {
              return "回答必須項目です。";
            } else if (x) {
              return (
                /^.+@.+$/.test(x) || "正しいメールアドレスを入力して下さい。"
              );
            }
          },
        ],
        パスワード: [
          (x) => {
            // if (!x) return true;
            if (!this.min) return true;
            return (
              (!!x && this.min <= x.length) ||
              `${this.min} 文字以上で入力してください。`
            );
          },
          (x) => {
            // if (!x) return true;
            if (!this.max) return true;
            return (
              (!!x && x.length <= this.max) ||
              `${this.max} 文字以内で入力してください。`
            );
          },
          (x) => {
            if (this.required && !x.trim()) {
              return "回答必須項目です。";
            } else {
              return true;
            }
          },
        ],
        電話番号: [
          (x) => {
            if (this.required && !x.trim()) {
              return "回答必須項目です。";
            } else if (x) {
              if (!x.match(/^[0-9-]+$/)) {
                return "正しい電話番号を入力してください。";
              }
            }
          },
        ],
        時間: [
          (x) => {
            if (this.required && !x.trim()) {
              return "回答必須項目です。";
            } else {
              return true;
            }
          },
        ],
        日付: [
          (x) => {
            if (this.required && !x.trim()) {
              return "回答必須項目です。";
            } else {
              return true;
            }
          },
        ],
        プルダウン選択: [
          (x) => {
            if (this.required && (this.multiple ? !x.length : !x.trim())) {
              return "回答必須項目です。";
            } else {
              return true;
            }
          },
        ],
      }[type].concat(additionalCheck);
    },
  },
};
</script>

<style scoped lang="scss">
::v-deep .phone-field {
  input[type="number"]::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
}
::v-deep .img-preview {
  border: 1px solid rgba(0, 0, 0, 0.38);
  border-radius: 5px;
  padding: 5px;
  margin-bottom: 20px;
  img {
    width: 100%;
  }
}
</style>
