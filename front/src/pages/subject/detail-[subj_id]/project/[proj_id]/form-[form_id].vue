<template>
    <div>
        <!-- <h2>Project detail - Preview</h2> -->
        <FormBase class="space-y-4 mt-2" :title="form?.title" :description="form?.description" @submit="handleSubmit">
            <!-- Loop through fields to render form fields -->
            <div v-for="(field, index) in form?.fields" :key="'preview-' + index">
                <label class="block font-medium mb-1">{{ field.label }}</label>

                <!-- Text field -->
                <FormTextField v-if="field.type === 'text'" v-model="assignInput[field.id].value" />

                <!-- Select field -->
                <FormSelectField v-else-if="field.type === 'select'" :options="getOptions(field)"
                    v-model="assignInput[field.id].value" />

                <!-- File upload -->
                <FormFileUploadField v-else-if="field.type === 'file'" v-model="assignInput[field.id].value" />

                <div v-if="field.type === 'file' && assignInput[field.id]?.value">
                    <!-- Render the file URL as a clickable download link -->
                    <a :href="assignInput[field.id].value?.toString()" target="_blank" class="text-blue-500">View
                        File</a>
                </div>
            </div>
        </FormBase>
    </div>
</template>
  

<script setup lang="ts">
import { useRoute } from 'vue-router'
import type { FormResponse, FormSubmissionPayload } from '@/types/interface'
import type { User } from '@/types/authInterface'

const auth = useAuthStore()
const route = useRoute()
const formId = route.params.form_id
const projectId = route.params.proj_id
const user = ref<User>()
const accessToken = ref()
const preValue = ref<Boolean>(false)
const form = ref<FormResponse>()
const assignInput = reactive<Record<number, { value: string | File | null; }>>({})

const editMode = ref(false);
const ToggleEdit = (): boolean => {
    return editMode.value = !editMode.value;
}

const handleSubmit = async () => {
    try {

        const formData = new FormData();
        formData.append('project_id', projectId.toString());
        formData.append('created_by_id', auth.user?.id?.toString() ?? '');
        formData.append('updated_by_id', auth.user?.id?.toString() ?? '');

        Object.entries(assignInput).forEach(([fieldId, input], index) => {
            formData.append(`fieldsResponse[${index}][form_field]`, fieldId);

            if (input.value instanceof File) {
                formData.append(`fieldsResponse[${index}][file]`, input.value);
                formData.append(`fieldsResponse[${index}][value]`, '');
            } else {
                formData.append(`fieldsResponse[${index}][value]`, input.value ?? '');
                formData.append(`fieldsResponse[${index}][file]`, '');
            }
        });


        await useFetch(`http://localhost:8000/project/submission/${formId}/assign`, {
            method: 'POST',
            body: formData,
            headers: {
                Authorization: `Bearer ${auth.accessToken}`
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
                    Authorization: `Bearer ${auth.accessToken}`,
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
                Authorization: `Bearer ${auth.accessToken}`,
            },
        }
    )
    if (res.data.value) {
        const submission = res.data.value as FormSubmission[];
        submission[0].fieldsResponse.forEach((item: FieldsResponse) => {
            if (assignInput[item.form_field.id]) {
                preValue.value = true
                assignInput[item.form_field.id].value = item.value || item.file;
            }
        })
    }
}

const getAuth = async () => {
    auth.loadFromCookies()
}

onMounted(async () => {
    await getAuth();
    await getAllForms();
    await getSubmission();

})

const getOptions = (field: any) => {

    return field.optionRaw?.split(',')
        .map((opt: string) => opt.trim())
        .filter((opt: string) => opt.length > 0)
        .map((opt: string) => ({ label: opt, value: opt })) || []
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