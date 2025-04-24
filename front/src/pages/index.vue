<template>
  <div>
    <p>Own Subject: {{ auth.ownSubject }}</p>
    <p>Own Project: {{ auth.ownProject }}</p>
    {{ auth.user?.role }}

    <!-- Navigation Buttons -->
    <div class="bg-blue-300 flex flex-wrap gap-2 p-4">
      <div class="p-2 bg-blue-300 hover:bg-blue-500 cursor-pointer"
        @click="navigateTo('/subject/detail-1/project/create')">
        Create Project
      </div>
      <div class="p-2 bg-blue-300 hover:bg-blue-500 cursor-pointer" @click="navigateTo('/subject/create')">
        Create Subject
      </div>
      <div class="p-2 bg-blue-300 hover:bg-blue-500 cursor-pointer" @click="navigateTo('/form/create')">
        Create Form
      </div>
      <div class="p-2 bg-blue-300 hover:bg-blue-500 cursor-pointer" @click="navigateTo('/form/link')">
        Link Form & Subject
      </div>
      <div class="p-2 bg-blue-300 hover:bg-blue-500 cursor-pointer" @click="navigateTo('/form/detail-20')">
        Form Detail Preview
      </div>
      <div class="p-2 bg-blue-300 hover:bg-blue-500 cursor-pointer" @click="navigateTo('/dashboard')">
        Dashboard
      </div>
      <div class="p-2 bg-blue-300 hover:bg-blue-500 cursor-pointer" @click="navigateTo('/subject/detail-1/project/9')">
        Project Detail
      </div>
      <div v-if="auth.ownProject && auth.ownSubject" class="p-2 bg-blue-300 hover:bg-blue-500 cursor-pointer"
        @click="navigateTo(`/subject/detail-${auth.ownSubject}/project/${auth.ownProject}`)">
        My Project Detail
      </div>
    </div>

    <!-- Subjects Grid -->
    <!-- v-if="Array.isArray(subjects) && subjects.length > 0" -->

    <!-- student -->
    <!-- have student role and not create project -->
    <div v-if="auth.user?.role == 'Student' && !auth.ownProject"
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 p-4">
      <div v-for="subject in subjects" :key="subject.id"
        class="bg-green-200 rounded-2xl shadow-md p-4 cursor-pointer hover:bg-green-300"
        @click="navigateTo(`/subject/detail-${subject.id}/project/create`)">
        <h2 class="text-lg font-semibold">{{ subject.name }}</h2>
        Student
        <p class="text-base text-gray-700">{{ subject.description }}</p>
      </div>
    </div>

    <!-- have student role and create project already -->
    <div v-if="auth.user?.role == 'Student' && auth.ownProject"
      class="flex flex-wrap gap-2 w-full max-w-[1000px] mx-auto p-6"> <!-- Wider max-w -->
      <div class="w-full mx-auto p-6">
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
          <div><strong>วิชา :</strong> {{ project?.subject_detail.name }}</div>
          <div><strong>นักศึกษา :</strong> {{ project?.student_detail.first_name + ' ' + project?.student_detail.last_name }}</div>
        </div>

        <!-- Main Form of Subject -->
        <div class="grid grid-cols-2 gap-4">
          <div v-for="formEntry in mainForm" :key="formEntry.id">
            <div v-for="field in formEntry.fieldsResponse" :key="field.id" class="py-4 bg-white rounded">
              <label class="block text-gray-700 font-semibold mb-1">{{ field.label }}</label>

              <div class="text-gray-800">
                <div v-if="getFieldAnswer(formEntry.field_responses, formEntry.submission, field.id, +auth.ownProject)">
                  {{ getFieldAnswer(formEntry.field_responses, formEntry.submission, field.id, +auth.ownProject) }}
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
            @click="navigateTo(`/subject/detail-${project?.student_detail.id}/project/${project?.id}/form-${form.id}`)">
            <div>
              <strong>{{ form.title }}</strong>
              <p>{{ form.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>



    <!-- Teacher -->
    <div v-if="auth.user?.role == 'Teacher'" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 p-4">
      <div v-for="subject in subjects" :key="subject.id"
        class="bg-green-200 rounded-2xl shadow-md p-4 cursor-pointer hover:bg-green-300"
        @click="navigateTo(`/subject/detail-${subject.id}/project/create`)">
        <h2 class="text-lg font-semibold">{{ subject.name }}</h2>
        Teacher
        <p class="text-base text-gray-700">{{ subject.description }}</p>
      </div>
    </div>
  </div>
</template>


<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import type { CreateProjectResponse, FormResponse, FormSubmission, ProjectResponse, SubjectResponse } from '../types/interface'

const router = useRouter()
const auth = useAuthStore()

const project = ref<CreateProjectResponse | null>(null)
const subjects = ref<SubjectResponse[]>([])

const listOfForm = ref<FormResponse[]>()
const mainForm = ref<FormSubjectResponse[]>()



const getAllSubjects = async () => {
  try {
    const res = await useFetch('http://localhost:8000/form/subject', {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
      },
    })
    subjects.value = res.data.value as SubjectResponse[]
  } catch (error) {
    console.error('Request failed:', error)
  }
}

const getProject = async () => {
  try {
    const res = await useFetch(`http://localhost:8000/project/${auth.ownProject}`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
      },
    })
    project.value = res.data.value as CreateProjectResponse
  } catch (err) {
    console.error('Get Project failed:', err)
  }
}

const getMainForm = async () => {
  try {
    const res = await useFetch(`http://localhost:8000/form/main-forms/${auth.ownSubject}`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${auth.accessToken}`
      }
    })
    // console.log('res', res.data.value)
    // console.log('path', `http://localhost:8000/form/main-forms/${subjectId}`)
    mainForm.value = res.data.value as FormSubjectResponse[]
  } catch (err) {
    console.error('Get Project failed:', err)
  }
}

const getFormOfSubject = async () => {
  try {
    const res = await useFetch(`http://localhost:8000/form/subject/${auth.ownSubject}/all-forms`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${auth.accessToken}`
      }
    })
    // console.log('res', res.data.value)
    listOfForm.value = res.data.value as FormResponse[]
    console.log('listOfForm', listOfForm)
    console.log('res.data.value', res.data.value)
  } catch (err) {
    console.error('Get Project failed:', err)
    // alert('Get Project failed')
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

const getAuth = async () => {
  auth.loadFromCookies()
}

onMounted(async () => {
  await getAuth();
  console.log("auth.ownSubject", auth.ownSubject)
  console.log("auth.ownProject", auth.ownProject)
  await getAllSubjects()

  if (auth.ownSubject || auth.ownProject) {
    await getProject()
    await getMainForm()
    await getFormOfSubject()

  }
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
