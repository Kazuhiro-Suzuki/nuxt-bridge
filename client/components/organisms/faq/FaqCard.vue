<template>
  <v-container>
    <v-row justify="center">
      <v-col sm="10" md="8" lg="8" xl="8">
        <v-card>
          <DenseToolBar
            :baseColor="baseColor"
            :title="title"
          />
          <v-col
            v-for="(item, i) in buttons"
            :key=i
            cols="12"
          >
            <MainMenuButton
              :i="i"
              :to="item.to"
              :imgFile="item.imgFile"
              :title="item.title"
              :type="item.type"
              color="grey lighten-4"
            />
          </v-col>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  props: {
    baseColor: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    buttons: {
      type: Array,
      required: true,
    },
  },
}
</script>
