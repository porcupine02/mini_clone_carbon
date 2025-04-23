<template>
    <div>
        <h2>Project detail - Preview</h2>
        <FormBase class="space-y-4 mt-2" :title="form?.title" :description="form?.description">
            <div v-for="(field, index) in form?.fields" :key="'preview-' + index">
                <label class="block font-medium mb-1">{{ field.label }}</label>
                <FormTextField v-if="field.type === 'text'" :edit="false" />
                <FormSelectField v-else-if="field.type === 'select'" :options="getOptions(field)" :edit="false" />
                <FormFileUploadField v-else-if="field.type === 'file'" :edit="false" />
            </div>
        </FormBase>

    </div>
</template>
    
<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
const formId = route.params.form_id
const user = ref()
const accessToken = ref()
const form = ref<FormResponse>()


interface FormFieldResponse {
    id: number;
    form: number;
    label: string;
    type: 'text' | 'select' | 'file';
    optionRaw: string | null;
    created_at: string;
    updated_at: string;
    created_by: number | null;
    updated_by: number | null;
}

interface FormResponse {
    id: number;
    title: string;
    description: string;
    main: number | null;
    created_at: string;
    updated_at: string;
    created_by: number | null;
    updated_by: number | null;
    fields: FormFieldResponse[];
}



const getAllSubjects = async () => {
    try {
        const res = await useFetch(
            `http://localhost:8000/form/${formId}`,
            {
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${accessToken.value}`,
                },
            }
        )

        form.value = res.data.value as FormResponse;
    } catch (error) {
        console.error('Request failed:', error);
    }
}


const getAuth = async () => {
    accessToken.value = localStorage.getItem('access_token') ?? ''
    const rawUser = localStorage.getItem('user')
    user.value = rawUser ? JSON.parse(rawUser) : null
}

onMounted(async () => {
    await getAuth()
    await getAllSubjects()

})


const getOptions = (field: any) => {
    // return field.optionsRaw?.split(',').map((item: string) => item.trim()) || []

    return field.optionsRaw?.split(',')
        .map((opt: string) => opt.trim())
        .filter((opt: string) => opt.length > 0)
        .map((opt: string) => ({ label: opt, value: opt })) || []
}

</script>