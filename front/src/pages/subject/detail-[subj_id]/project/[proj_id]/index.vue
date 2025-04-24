<template>
    <div class="max-w-4xl mx-auto p-6">
        <div class="mb-4">
            <h1 class="text-3xl font-bold">{{ project?.title_th }}</h1>
            <p class="text-xl text-gray-700">{{ project?.title_en }}</p>
        </div>

        <!-- Keyword -->
        <div class="mb-4">
            <div class="flex flex-wrap gap-2">
                <span v-for="(word, idx) in project?.keyword || []" :key="idx"
                    class="px-3 py-1 bg-gray-100 rounded-full text-sm text-gray-800 border">
                    {{ word }}
                </span>
            </div>
        </div>

        <!-- Subject -->
        <div class="grid grid-cols-2 gap-4 mt-6">
            <div><strong>วิชา :</strong> {{ project?.subject.name }}</div>
            <div><strong>นักศึกษา :</strong> {{ project?.student.first_name + ' ' + project?.student.last_name }}</div>
        </div>


        <!-- Main Form of Subject -->
        <div class="grid grid-cols-2 gap-4">
            <div v-for="formEntry in mainForm" :key="formEntry.id">
                <div v-for="field in formEntry.fieldsResponse" :key="field.id" class="py-4 bg-white rounded">
                    <label class="block text-gray-700 font-semibold mb-1">{{ field.label }}</label>

                    <div class="text-gray-800">
                        <div v-if="getFieldAnswer(formEntry.field_responses, formEntry.submission, field.id, +projectId)">
                            {{ getFieldAnswer(formEntry.field_responses, formEntry.submission, field.id, +projectId) }}
                        </div>
                        <div v-else>
                            <p class="text-gray-400">No response</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>


        <!-- Assignments -->
        <div class="w-full mt-6">
            <strong class="mt-3">Assignments</strong>
            <div v-for="form in listOfForm" :key="form.id" class="pl-6 py-3 hover:bg-gray-50"
                @click="navigateTo(`/subject/detail-${project?.subject.id}/project/${project?.id}/form-${form.id}`)">
                <div>
                    <strong>{{ form.title }}</strong>
                    <p>{{ form.description }}</p>
                </div>
            </div>
        </div>
    </div>
</template>
  
    
<script setup lang="ts">
import { useRoute } from 'vue-router'
import type { ProjectResponse, FormResponse, FormSubmission } from '@/types/interface'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const projectId = route.params.proj_id
const subjectId = route.params.subj_id
const project = ref<ProjectResponse>()
const listOfForm = ref<FormResponse[]>()

const mainForm = ref<FormSubjectResponse[]>()

const user = ref()
const accessToken = ref()


const getAuth = async () => {
    accessToken.value = localStorage.getItem('access_token') ?? ''
    const rawUser = localStorage.getItem('user')
    user.value = rawUser ? JSON.parse(rawUser) : null
}

const getProject = async () => {
    try {
        const res = await useFetch(`http://localhost:8000/project/${projectId}`, {
            method: 'GET',
            headers: {
                Authorization: `Bearer ${accessToken.value}`
            }
        })
        project.value = res.data.value as ProjectResponse
    } catch (err) {
        console.error('Get Project failed:', err)
        // alert('Get Project failed')
    }
}

const getFormOfSubject = async () => {
    try {
        const res = await useFetch(`http://localhost:8000/form/subject/${auth.ownSubject}/all-forms`, {
            method: 'GET',
            headers: {
                Authorization: `Bearer ${accessToken.value}`
            }
        })
        listOfForm.value = res.data.value as FormResponse[]
    } catch (err) {
        console.error('Get Project failed:', err)
        // alert('Get Project failed')
    }
}

const getMainForm = async () => {
    try {
        const res = await useFetch(`http://localhost:8000/form/main-forms/${subjectId}`, {
            method: 'GET',
            headers: {
                Authorization: `Bearer ${accessToken.value}`
            }
        })
        mainForm.value = res.data.value as FormSubjectResponse[]
    } catch (err) {
        console.error('Get Project failed:', err)
    }
}


const getFieldAnswer = (
    fieldResponses: FormFieldSubmit[],
    submissions: FormSubmission[],
    fieldId: number,
    projectId: number
): string | null => {
    const validSubmissionIds = submissions
        .filter(sub => sub.project === projectId)
        .map(sub => sub.id)

    const res = fieldResponses.find(
        r => r.form_field === fieldId && validSubmissionIds.includes(r.form_submission)
    )


    if (!res) return null

    // If it has a file, will return that, otherwise return filepath
    if (res.file) return `Uploaded file: ${res.file}`
    return res.value || null
}

onMounted(async () => {
    await getAuth();
    await getProject();
    await getFormOfSubject();
    await getMainForm();
})

const navigateTo = (path: string) => {
  router.push(path)
}
interface FormField {
    id: number;
    form: number;
    label: string;
    type: string;
    optionRaw: string | null;
    created_at: string;
    updated_at: string;
    created_by: number | null;
    updated_by: number | null;
}

interface Form {
    id: number;
    subjects: number[];
    title: string;
    description: string;
    main: boolean | null;
    created_at: string;
    updated_at: string;
    created_by: number | null;
    updated_by: number | null;
}

interface FormSubjectResponse {
    id: number;
    form: Form;
    main: boolean;
    subject: number;
    fieldsResponse: FormField[];
    submission: FormSubmission[];
    field_responses: FormFieldSubmit[];
}

interface FormFieldSubmit {
    id: number;
    form_submission: number;
    form_field: number;
    value: string | null;
    file: string | null;
    created_at: string;
    updated_at: string;
    created_by: number | null;
    updated_by: number | null;
}

</script>