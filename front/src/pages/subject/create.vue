<template>
    <div class="max-w-2xl mx-auto p-6 bg-white shadow-md rounded-lg mt-10">
        <h2 class="text-2xl font-bold mb-6 text-gray-800">Create Subject</h2>

        <form @submit.prevent="submitSubject" class="space-y-4">
            <FormTextField label="Subject Name" placeholder="Enter subject name" v-model="subject.name" />

            <FormTextField label="Description" placeholder="Enter subject description" v-model="subject.description" />

            <div class="flex justify-end">
                <button type="submit" class="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
                    Create Subject
                </button>
            </div>
        </form>
    </div>
</template>
  
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const subject = ref({
    name: '',
    description: '',
})


// const user = ref()
// const accessToken = ref()

const auth = useAuthStore()

const getAuth = async () => {
    auth.loadFromCookies()
}
onMounted(async () => {

    await getAuth();

})

const submitSubject = async () => {
    try {
        const payload = {
            ...subject.value,
            created_by: auth.user?.id,
            updated_by: auth.user?.id,
        }
        console.log('payload', payload)
        console.log('accessToken', auth.accessToken)
        const res = await useFetch('http://localhost:8000/form/subject', {
            method: 'POST',
            body: payload,
            headers: {
                Authorization: `Bearer ${auth.accessToken}`
            }
        })
        if (res.error.value?.message) {
            throw new Error(res.error.value?.message);
        }
        alert('Subject created successfully!')
        // router.push('/admin/subjects')
    } catch (error) {
        console.error(error)
        alert('Failed to create subject.')
    }
}
</script>