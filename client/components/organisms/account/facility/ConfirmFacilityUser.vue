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
            <v-text-field
              v-if="data.email"
              v-model="data.email"
              label="メールアドレス"
              outlined
              :rules="[$rules.required]"
              :readonly="readonly"
              :filled="readonly"
            ></v-text-field>
            <v-autocomplete
              v-if="data.facilities"
              v-model="data.facilities"
              return-object
              label="施設名"
              :items="items"
              item-text="name"
              item-value="id"
              outlined
              multiple
              :rules="[$rules.required]"
              :readonly="readonly"
              :filled="readonly"
              :search-input.sync="search"
              @change="search = ''"
            ></v-autocomplete>
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
        :isNormalButton="true"
        :btnClass="btnClass"
        :title="confirmTitle"
        :baseColor="baseColor"
        :darkColor="darkColor"
        :buttonText="confirmButtonText"
        @clickAction1="clickEvent2Method"
      >
        <template v-slot:userInfo>
          <slot name="confirmText"></slot>
        </template>
        <template v-slot:firstAction>
          <slot name="firstAction"></slot>
        </template>
      </Confirmation>
    </v-dialog>

  </v-card>
</template>

<script>

export default {
  props: {
    title: {
      type: String,
      required: true,
    },
    confirmTitle: {
      type: String,
      required: false,
    },
    confirmButtonText: {
      type: String,
      required: false,
    },
     btnClass: {
      type: String,
      required: false,
    },
    baseColor: {
      type: String,
      required: true,
    },
    darkColor: {
      type: String,
      required: true,
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
    items: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      dialog: false,
      dialogWidth: '400',
      formValid: false,
      search: null,
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