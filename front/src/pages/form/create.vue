<template>
    <div>
        <h1 class="text-2xl font-bold mb-6">Admin - Create Form</h1>
        <FormTextField label="Title" v-model="title" />
        <FormTextField label="Description" v-model="description" />
        <FormBuilder :pre_title="title" :pre_des="description" @update:fields="fields = $event" />


        <div class="w-full flex justify-center py-4 sticky bottom-0 bg-white border-t">
            <button class="flex justify-end px-4 py-2 bg-green-600 text-white rounded" @click="submitForm">
                Submit Form
            </button>
        </div>
    </div>
</template>
  
<script setup lang="ts">
const title = ref("")
const description = ref("")
const fields = ref([])
const user = ref()
const accessToken = ref()
const auth = useAuthStore()

const getAuth = async () => {
    auth.loadFromCookies()
}
onMounted(async () => {
    await getAuth()
    accessToken.value = localStorage.getItem('access_token')
    const rawUser = localStorage.getItem('user')
    user.value = rawUser ? JSON.parse(rawUser) : null

})
const submitForm = async () => {
    try {
        const payload = {
            form: {
                title: title.value,
                description: description.value,
                created_by: auth.user?.id,
                updated_by: auth.user?.id,
            },
            fields: fields.value,
            created_by: auth.user?.id,
            updated_by: auth.user?.id,
        }

        const { data, error } = await useFetch('http://localhost:8000/form/with-fields', {
            method: 'POST',
            body: payload,
            headers: {
                Authorization: `Bearer ${accessToken.value}`
            }
        })

        alert("Create form success.")
    } catch (err) {
        console.error('Error submitting form:', err)
    }
}
</script>