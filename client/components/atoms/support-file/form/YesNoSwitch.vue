<template>
  <v-container class="px-0 py-1">
    <v-row no-gutters>
      <v-col cols="6" class="px-1">
        <input
          :id="noId"
          v-model="radioPresenceValue"
          type="radio"
          :name="radioName"
          value="no"
          data-testid="radio-no"
          @change="changea()"
        />
        <label :for="noId">
          {{ noLabel }}
        </label>
      </v-col>
      <v-col cols="6" class="px-1">
        <input
          :id="yesId"
          v-model="radioPresenceValue"
          type="radio"
          :name="radioName"
          value="yes"
          data-testid="radio-yes"
          @change="changea()"
        />
        <label :for="yesId">
          {{ yesLabel }}
        </label>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
function randomName() {
  return Math.random()
    .toString(32)
    .substring(2)
}

export default {
  name: 'YesNoSwitch',
  model: {
    prop: 'value',
    event: 'change'
  },
  props: {
    yesLabel: {
      type: String,
      default: 'はい'
    },
    noLabel: {
      type: String,
      default: 'いいえ'
    },
    value: {
      type: [Boolean, String, Number, Object],
      default: null
    },
    radioName: {
      type: String,
      default: randomName()
    }
  },
  computed: {
    radioPresenceValue: {
      get() {
        return this.value ? 'yes': 'no'
      },
      set(newValue) {
        this.$emit('change', newValue === 'yes')
      }
    }
  },
  methods: {
    changea(){
      console.log("aaaa")
    }
  },
  data() {
    return {
      noId: randomName(),
      yesId: randomName()
    }
  },
}
</script>

<style lang="scss" scoped>
label {
  display: block;
  padding: 15px;
  box-sizing: border-box;
  border: 1px solid #dce1e6;
  border-radius: 5px;
  color: #000000;
  background-color: #ffffff;
  text-align: center;
}

.disabled {
  label {
    border: 1px solid #eee;
    background-color: #eee;
  }
  input:checked + label {
    background: #ffffff;
    border: 1px solid #000000;
  }
}

input {
  position: fixed;
  top: -100%;
  left: -100%;
  display: block;
  width: 0;
  height: 0;
  visibility: hidden;
  border: none;

  &:checked + label {
    background: #F0FCF5;
    border: 1px solid #118C46;
    color: #118C46;
  }
}

.hidden {
  visibility: hidden;
  display: none;
}
</style>
