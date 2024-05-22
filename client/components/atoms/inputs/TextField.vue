<template>
	<v-text-field
    v-model="textFieldData"
		outlined
		counter
    :background-color="backgroundColor"
		:label="label"
    :placeholder="placeholder"
		:maxlength="maxlength"
    :rules="rules"
    :prepend-inner-icon="icon"
    :append-icon="appendIcon"
    :type="type"
    :disabled="disabled"
    @click:append="$emit('clickAction')"
	></v-text-field>
</template>
<script>
export default {
	props: {
		label: {
      type: String,
      required: true,
    },
    placeholder: {
      type: String,
      required: false,
    },
		maxlength: {
      type: String,
      required: false,
    },
    backgroundColor: {
      type: String,
      required: false,
    },
    rules: {
      type: Array,
      required: false,
    },
    icon: {
      type: String,
      required: false,
    },
    appendIcon: {
      type: String,
      required: false,
    },
    type: {
      type: String,
      required: false,
    },
    disabled: {
      type: Boolean,
      required: false,
    }
  },
  data() {
    return {
      textFieldData: ''
    }
  },
  watch: {
    textFieldData: function(value) {
      this.$emit('textFieldData', value)
    }
  }
}
</script>
