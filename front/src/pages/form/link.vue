<template>
    <div class="p-4">
        <h1 class="text-xl font-bold mb-4">Link Form to Subject</h1>
        <!-- Subjects -->
        <label class="block mb-2">Select Subject:</label>
        <select v-model="selectedSubjectId" class="mb-4 p-2 border rounded w-full">
            <option disabled value="">-- Choose Subject --</option>
            <option v-for="subj in subjects" :key="subj.id" :value="subj.id">
                {{ subj.name }}
            </option>
        </select>
        <label class="block mb-2">Select Form(s):</label>
        <div v-for="form in forms" :key="form.id" class="grid grid-cols-12 items-center gap-4 mb-2">
            <!-- Checkbox + Form Title -->
            <div class="col-span-5 flex items-center gap-2">
                <input type="checkbox" :id="`form-${form.id}`" :value="form.id" v-model="selectedFormIds" />
                <label :for="`form-${form.id}`" class="font-medium">{{ form.title }}</label>
            </div>

            <!-- Unlink -->
            <div class="col-span-2" v-if="preSelectedFormIds.includes(form.id)">
                <button @click="unlink(form.id)" class="text-red-500 underline text-sm">Unlink</button>
            </div>
            <div class="col-span-2" v-else>
            </div>

            <!-- Main Checkbox -->
            <div class="col-span-5 flex items-center gap-2">
                <input type="checkbox" :id="`main-${form.id}`" :checked="mainFormIds.includes(form.id)"
                    :disabled="!selectedFormIds.includes(form.id)" @change="() => toggleMain(form.id)" />
                <label :for="`main-${form.id}`" class="text-sm text-gray-600">Main</label>
            </div>

            <!-- Date -->
            <div class="col-span-5 flex items-center gap-2">
                <input type="date" :id="`main-${form.id}`" :checked="mainFormIds.includes(form.id)"
                    :disabled="!selectedFormIds.includes(form.id)" @change="() => toggleMain(form.id)" />
                <label :for="`main-${form.id}`" class="text-sm text-gray-600">Main</label>
            </div>
        </div>


        <button @click="linkFormsToSubject" class="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
            Link
        </button>
    </div>
</template>
  
<script setup lang="ts">
const auth = useAuthStore()
const forms = ref<FormResponse[]>([])
const subjects = ref<SubjectResponse[]>([])
const selectedFormIds = ref<number[]>([])
const preSelectedFormIds = ref<number[]>([])
const selectedSubjectId = ref<number | null>(null)
const listLink = ref<listLink[]>([])
const mainFormIds = ref<number[]>([])


interface SubjectResponse {
    id: number;
    name: string;
    forms: FormResponse[];
    created_at: string;
    updated_at: string;
    created_by: string;
    updated_by: string;
}
interface FormResponse {
    id: number;
    subjects: number[];
    title: string;
    description: string;
    // main: string;
    created_at: string;
    updated_at: string;
    created_by: string;
    updated_by: string;
}

interface listLink {
    id: number;
    form: number;
    main: Boolean;
    subject: number;
    starttime?: Date;
    endtime?: Date;
}
const getLinkFormSubject = async () => {
    const res = await useFetch(
        'http://localhost:8000/form/link-form-subject',
        {
            method: 'GET',
            headers: {
                Authorization: `Bearer ${auth.accessToken}`,
            },
        }
    )
    console.log(res.data.value)
    listLink.value = res.data.value as listLink[];
}
const findIdFormSubjectLink = (subj_id: number, form_id: number): number => {
    return listLink.value.find(link => link.subject === subj_id && link.form === form_id)?.id || 0
}

const toggleMain = async (form_id: number) => {
    const formSubjId = findIdFormSubjectLink(selectedSubjectId.value ?? 0, form_id)
    const isCurrentlyMain = mainFormIds.value.includes(form_id)
    const payload = {
        main: !isCurrentlyMain
    }
    await useFetch(`http://localhost:8000/form/add-main/${formSubjId}`, {
        method: 'PATCH',
        body: payload,
        headers: {
            Authorization: `Bearer ${auth.accessToken}`,
        },
    })
    await getLinkFormSubject()
    mainFormIds.value = listLink.value
        .filter(link => link.subject === selectedSubjectId.value && link.main)
        .map(link => link.form)

}


const unlink = async (formId: number) => {
    const payload = {
        form_ids: [formId],
        created_by: auth.user?.id,
        updated_by: auth.user?.id,

    }
    try {
        const res = await useFetch(`http://localhost:8000/form/subject/${selectedSubjectId.value}/add-forms`, {
            method: 'DELETE',
            body: payload,
            headers: {
                Authorization: `Bearer ${auth.accessToken}`
            }
        })
        window.location.reload();
        // await getAllSubjects()
        // await getAllForms()

    } catch (err) {
        console.error('Project creation failed:', err)
        alert('Project creation failed')
    }

}


const linkFormsToSubject = async () => {

    const payload = {
        form_ids: selectedFormIds.value,
        created_by: auth.user?.id,
        updated_by: auth.user?.id,
    }
    try {
        const res = await useFetch(`http://localhost:8000/form/subject/${selectedSubjectId.value}/add-forms`, {
            method: 'POST',
            body: payload,
            headers: {
                Authorization: `Bearer ${auth.accessToken}`
            }


        })

        window.location.reload();
        // await getAllSubjects()
    } catch (err) {
        console.error('Project creation failed:', err)
        alert('Project creation failed')
    }
}

watch(selectedSubjectId, async (newVal) => {
    const subject = subjects.value.find(s => s.id === newVal)
    if (subject) {
        selectedFormIds.value = subject.forms.map(f => f.id)
        preSelectedFormIds.value = subject.forms.map(f => f.id)
    }
    await getLinkFormSubject()
    mainFormIds.value = listLink.value
        .filter(link => link.subject === selectedSubjectId.value && link.main)
        .map(link => link.form)

})

const getAllForms = async () => {
    try {
        const res = await useFetch(
            'http://localhost:8000/form',
            {
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${auth.accessToken}`,
                },
            }
        )

        forms.value = res.data.value as FormResponse[];
    } catch (error) {
        console.error('Request failed:', error);
    }
}

const getAllSubjects = async () => {
    try {
        const res = await useFetch(
            'http://localhost:8000/form/subject',
            {
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${auth.accessToken}`,
                },
            }
        )

        subjects.value = res.data.value as SubjectResponse[];
    } catch (error) {
        console.error('Request failed:', error);
    }
}


const getAuth = async () => {
    auth.loadFromCookies()
}



onMounted(async () => {
    await getAuth()
    await getAllForms()
    await getAllSubjects()


    if (subjects.value.length > 0) {
        selectedSubjectId.value = subjects.value[0].id
    }
})

</script>
