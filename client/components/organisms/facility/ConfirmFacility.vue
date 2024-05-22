<template>
  <v-card>
    <DenseToolBar
      :title="title"
      :baseColor="baseColor"
    />

    <v-row>
      <v-col>
        <v-card-text>
          <v-form v-model="formValid">
            <!-- <v-text-field
              v-model="data.postal_code"
              label="郵便番号"
              outlined
              counter
              maxlength="7"
              :rules="[$rules.required]"
              :readonly="readonly"
              :filled="readonly"
            ></v-text-field>

            <v-text-field
              v-model="data.phone_number"
              label="電話番号"
              outlined
              counter
              maxlength="15"
              :rules="[$rules.required]"
              :readonly="readonly"
              :filled="readonly"
            ></v-text-field>

            <v-text-field
              v-model="data.address"
              label="住所"
              outlined
              counter
              maxlength="100"
              :rules="[$rules.required]"
              :readonly="readonly"
              :filled="readonly"
            ></v-text-field> -->

            <v-text-field
              v-model="data.name"
              label="名称"
              outlined
              counter
              maxlength="100"
              :rules="[$rules.required]"
              :readonly="readonly"
              :filled="readonly"
              background-color="white"
            ></v-text-field>

          </v-form>
        </v-card-text>
      </v-col>
    </v-row>

    <v-divider></v-divider>

    <div>
      <v-card-actions
        class="justify-center"
      >
        <div v-if="buttonText=='閉じる'">
          <TextButton
            :text="buttonText"
            :color="darkColor"
            @clickEvent1="$emit('clickEvent3')"
          />
        </div>
        <div v-else>
          <TextButton
            :text="buttonText"
            :color="darkColor"
            :disabled="!formValid"
            @clickEvent1="dialog = !dialog"
          />
        </div>
      </v-card-actions>
    </div>

    <v-dialog
      v-model="dialog"
      :width="dialogWidth"
    >
      <Confirmation
        title="確認"
        :baseColor="baseColor"
        :darkColor="darkColor"
        buttonText="確定する"
        @clickEvent2="clickEvent2Method"
      />
    </v-dialog>

  </v-card>
</template>

<script>
import VueCtkDateTimePicker from 'vue-ctk-date-time-picker'

export default {
  components: {
    VueCtkDateTimePicker,
  },
  props: {
    title: {
      type: String,
      required: true,
    },
    baseColor: {
      type: String,
      required: true,
    },
    darkColor: {
      type: String,
      required: false,
    },
    data: {
      type: Object,
      required: true
    },
    buttonText: {
      type: String,
      required: false,
    },
    readonly: {
      type: Boolean,
      required: false,
    },
  },
  data() {
    return {
      dialog: false,
      dialogWidth: '400',
      formValid: false,
    }
  },
  methods: {
    clickEvent2Method() {
      this.dialog = false
      this.$emit('clickEvent3')
    }
  }
}
</script>