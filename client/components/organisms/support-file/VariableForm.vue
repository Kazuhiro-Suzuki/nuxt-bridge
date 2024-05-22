<template>
  <v-form ref="form">
    <v-row
      v-for="(section, i) in sections"
      :key="i + ':' + section.sectionName"
    >
      <VariableTypeSelection
        :answer="repl"
        :type="section.type" 
        :section="section" 
        :fluctuation="section.fluctuation"
        @change="change"/>
    </v-row>
  </v-form>
</template>

<script>
import VariableTypeSelection from "@/components/molecules/support-file/VariableTypeSelection.vue"
export default {
  name: "VariableForm",
  components: {
    VariableTypeSelection,
  },
  filters: {},
  computed: {},
  mounted() {
  },
  created() {
    
  },
  watch: {
  },
  props: {
    sections: {
      type:Array,
      default: function () {
        return []
      },
    },
    repl: {
      type: Object,
      default: function () {
        return {}
      },
    }
  },
  computed: {
  },
  data() {
    return {
    }
  },
  methods: {
    change(event) {
      this.$emit("change", Object.assign(this.repl, event))
    }
  },
};
</script>

<style scoped>
.description {
  display: block;
  color: #8a8a8a;
}

.section-title {
  text-align: left;
  font: normal normal normal 16px/24px Hiragino Sans;
  letter-spacing: 0px;
  color: #212121;
  opacity: 1;
  font-weight: 300;
}

.field-label {
  text-align: left;
  font: normal normal normal 16px/24px Hiragino Sans;
  letter-spacing: 0px;
  color: #212121;
  opacity: 1;
  font-weight: 600;
  white-space: normal;
}
</style>
