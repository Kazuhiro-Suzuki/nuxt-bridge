<template>
    <v-file-input @change="imageToBase64($event)" :accept="accept" :prepend-icon="icon" :label="label"></v-file-input>                
</template>
<script>
export default {
    name: 'SelectionSwitch',
    model: {
        prop: 'inputData',
        event: 'change'
    },
    props: {
        inputData: {
            type: String,
            default: null
        },
        accept: {
            type: String,
            default: null
        },
        icon: {
            type: String,
            default: null
        },
        label: {
            type: String,
            default: null
        }
    },
    methods: {
        imageToBase64(event) {
            console.log(event)
            const reader = new FileReader()

            // ファイルが選択されていればBase64に変換する
            if (event) {
                reader.readAsDataURL(event)
            } else {
                this.previewBase64 = ''
            }

            // 変換が終わったら実行される
            reader.onload = () => {
                this.$emit('change', reader.result)
                console.log(reader.result)
            }
        }
    }
}
</script>