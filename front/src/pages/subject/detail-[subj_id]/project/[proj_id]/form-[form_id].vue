<template>
    <div>
        <h2>Project detail - Preview</h2>
        <FormBase class="space-y-4 mt-2" :title="form?.title" :description="form?.description" @submit="handleSubmit">
            <div v-for="(field, index) in form?.fields" :key="'preview-' + index">
                <label class="block font-medium mb-1">{{ field.label }}</label>
                <FormTextField v-if="field.type === 'text'" v-model="assignInput[field.id].value" :edit="true" />
                <FormSelectField v-else-if="field.type === 'select'" :options="getOptions(field.optionRaw)"
                    v-model="assignInput[field.id].value" :edit="true" />
                <FormFileUploadField v-else-if="field.type === 'file'" v-model="assignInput[field.id].value" :edit="true" />
            </div>
        </FormBase>


    </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import type { FormResponse, FormSubmissionPayload } from '@/types/interface'
import type { User } from '@/types/authInterface'

const route = useRoute()
const formId = route.params.form_id
const projectId = route.params.proj_id
const user = ref<User>()
const accessToken = ref()
const preValue = ref<Boolean>(false)
const form = ref<FormResponse>()
const assignInput = reactive<Record<number, { value: string | File | null }>>({})


const handleSubmit = async () => {
    try {

        const payload: FormSubmissionPayload = {
            project_id: +projectId,
            fieldsResponse: Object.entries(assignInput).map(([fieldId, input]) => ({
                form_field: Number(fieldId),
                value: typeof input.value === 'string' ? input.value : null,
                file: input.value instanceof File ? input.value.name : null
            })),
            created_by_id: user.value?.id ?? null,
            updated_by_id: user.value?.id ?? null,
        }


        await useFetch(`http://localhost:8000/project/submission/${formId}/assign`, {
            method: 'POST',
            body: payload,
            headers: {
                Authorization: `Bearer ${accessToken.value}`
            }
        })
    } catch (err) {
        console.error('Error submitting form:', err)
    }
}

const getAllForms = async () => {
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
        form.value.fields.forEach(field => {
            assignInput[field.id] = { value: null };
        });

    } catch (error) {
        console.error('Request failed:', error);
    }
}

const getSubmission = async () => {
    const res = await useFetch(
        `http://localhost:8000/project/submission/project/${projectId}/form/${formId}`,
        {
            method: 'GET',
            headers: {
                Authorization: `Bearer ${accessToken.value}`,
            },
        }
    )
    if (res.data.value) {
        const submission = res.data.value as FormSubmission[];
        submission[0].fieldsResponse.forEach((item: FieldsResponse) => {
            if (assignInput[item.form_field.id]) {
                preValue.value = true
                assignInput[item.form_field.id].value = item.value;
            }
        })
    }
}

const getAuth = async () => {
    accessToken.value = localStorage.getItem('access_token') ?? ''
    const rawUser = localStorage.getItem('user')
    user.value = rawUser ? JSON.parse(rawUser) : null
}

onMounted(async () => {
    await getAuth();
    await getAllForms();
    await getSubmission();

})

const getOptions = (optionRaw: string | string[] | null): { label: string; value: string }[] => {
    if (typeof optionRaw === 'string') {
        try {
            const parsed = JSON.parse(optionRaw);
            if (Array.isArray(parsed)) {
                return parsed.map(opt => ({ label: opt, value: opt }));
            }
        } catch (e) {
            console.error('Invalid JSON in optionRaw:', optionRaw);
        }
        return [];
    }

    if (Array.isArray(optionRaw)) {
        return optionRaw.map(opt => ({ label: opt, value: opt }));
    }

    return [];
}

interface FormField {
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

interface FieldsResponse {
    id: number;
    form_field: FormField;
    value: string | null;
    file: string | null;
    created_at: string;
    updated_at: string;
    form_submission: number;
    created_by: number;
    updated_by: number;
}

interface Form {
    id: number;
    subjects: number[];
    title: string;
    description: string;
    main: string | null;
    created_at: string;
    updated_at: string;
    created_by: number | null;
    updated_by: number | null;
}

interface FormSubmission {
    id: number;
    form: Form;
    fieldsResponse: FieldsResponse[];
    status: 'Pending' | 'Approved' | 'Rejected';
    created_at: string;
    updated_at: string;
    project: number;
    approve_by: number | null;
    created_by: number;
    updated_by: number;
}
</script>