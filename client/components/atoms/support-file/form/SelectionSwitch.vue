<template>
  <v-container class="px-0 py-1">
    <v-row no-gutters :class="{ disabled: disabled }">
      <v-col v-for="option in options" :key="option" class="px-1">
        <input
          :id="option+ radioName"
          v-model="radioPresenceValue"
          type="radio"
          :name="radioName"
          :value="option"
          :disabled="disabled"
        />
        <label :for="option+ radioName">
          {{ option }}
        </label>
      </v-col>
    </v-row>
    <input
      v-model="radioPresenceValue"
      type="radio"
      class="hidden"
      :name="radioName"
      value="__empty__"
      data-testid="radio-empty"
      :disabled="disabled"
    />
  </v-container>
</template>

<script>
function randomName() {
  return Math.random()
    .toString(32)
    .substring(2)
}

export default {
  name: 'SelectionSwitch',
  model: {
    prop: 'value',
    event: 'change'
  },
  props: {
    options: {
      type: Array,
      required: true
    },
    value: {
      type: String,
      default: 'いいえ'
    },
    radioName: {
      type: String,
      default: randomName
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    radioPresenceValue: {
      get() {
        return this.value || '__empty__'
      },
      set(newValue) {
        if (newValue === '__empty__') {
          this.$emit('change', null)
        } else {
          this.$emit('change', newValue)
        }
      }
    }
  }
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
