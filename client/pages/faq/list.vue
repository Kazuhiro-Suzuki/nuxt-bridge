<template>
  <v-container>
    <v-row justify="center">
      <v-col sm="10" md="8" lg="8" xl="8">
        <v-card>
          <DenseToolBar
            :baseColor="regionData.base_color"
            :title="title"
          />
          <v-card-text>
            <v-row justify="center" v-if="faqCategories.length != 1 || (faqCategories.length == 1 && faqCategories[0].id)">
              <v-col cols="12" v-for="category in faqCategories"
                :key="category.id">
                <v-card v-if="category.faqItems && category.faqItems.length">
                  <v-card class="elevation-0 lighten-4 font-weight" :color='regionData.base_color'>
                    <v-card-title>{{ category.name }}</v-card-title>
                  </v-card>
                    <v-card-text>
                      <v-row justify="center">
                        <v-col>
                          <v-row>
                            <v-col
                              cols="12"
                              v-for="(item, i) in category.faqItems"
                              :key="i"
                            >
                              <v-card color="grey lighten-4">
                                <v-card-title>
                                  Q.{{ item.question }}
                                </v-card-title>
                                <v-divider></v-divider>
                                <v-card-subtitle>
                                  A.{{ item.answer }}
                                </v-card-subtitle>
                              </v-card>
                            </v-col>
                          </v-row>
                        </v-col>
                      </v-row>
                    </v-card-text>
                </v-card>
              </v-col>
            </v-row>
            <v-row justify="center" v-else>
              <v-col
                v-for="(item, i) in faqCategories[0].faqItems"
                :key=i
                cols="12"
              >
                <v-card color="grey lighten-4">
                  <v-card-title>
                    Q.{{ item.question }}
                  </v-card-title>
                  <v-divider></v-divider>
                  <v-card-subtitle>
                    A.{{ item.answer }}
                  </v-card-subtitle>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  meta: {
    back: true
  },
  head() {
    return {
      title: this.title
    }
  },
  data() {
    return {
      citycode: this.$route.query.citycode,
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
  },
  async asyncData({ route, $api }) {
    let title = ''
    let faqCategories = []
    let errorMessage = ''
    const response = await $api.getFAQ(`${route.query.citycode}`)
    // console.log(response.data)
    if (response.status === 200) {
      faqCategories = response.data
    } else {
      if (response.data.detail) {
        errorMessage = response.data.detail
      } else {
        errorMessage = 'サーバーエラーです、時間置いてからお試しください。'
      }
    }

    if(route.query.citycode == '142077'){
      title= '本アプリや行政手続き等について'
      
      const index = faqCategories.findIndex(category => category.id === 8);
      if (index !== -1) {
        const elementToMove = faqCategories.splice(index, 1)[0];
        faqCategories.unshift(elementToMove);
      }
    }else{
      title = '本アプリについて'
    }

    console.log(faqCategories);
    
    return {
      title,
      faqCategories,
      errorMessage,
    }
  },
}
</script>
