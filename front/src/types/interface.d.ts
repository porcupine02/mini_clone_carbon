export interface FormFieldResponse {
  id: number;
  form: number;
  label: string;
  type: "text" | "select" | "file";
  optionRaw: string | string[] | null;
  created_at: string;
  updated_at: string;
  created_by: number | null;
  updated_by: number | null;
}

export interface FormResponse {
  id: number;
  title: string;
  description: string;
  main: number | null;
  starttime: Date;
  endtime: Date;
  created_at: string;
  updated_at: string;
  created_by: number | null;
  updated_by: number | null;
  fields: FormFieldResponse[];
}

export interface SubjectResponse {
  id: number;
  name: string;
  description: string;
  created_at: string;
  updated_at: string;
  created_by: number | null;
  updated_by: number | null;
  forms: FormResponse[];
}

export interface ProjectResponse {
  id: number;
  title_th: string;
  title_en: string;
  keyword: string[];
  created_at: string;
  updated_at: string;
  subject: SubjectResponse;
  student: UserResponse;
  created_by: number;
  updated_by: number;
}

export interface CreateProjectResponse {
  id: number;
  title_th: string;
  title_en: string;
  keyword: string[];
  created_at: string;
  updated_at: string;
  subject_detail: SubjectResponse;
  student_detail: User;
  teacher_detail: User;
  created_by: number;
  updated_by: number;
}

export interface UserResponse {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
}

export interface FieldResponse {
  value: string | null;
  form_field: number; // form_field_id
  file: string | null;
}

export interface FormSubmissionPayload {
  project_id: number;
  fieldsResponse: FieldResponse[];
  created_by_id: number | null;
  updated_by_id: number | null;
}

export interface FormField {
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


export interface FormFieldSubmit {
  id: number;
  form_submission: number;
  form_field: FormField;
  value: string | null;
  file: string | null;
  created_at: string;
  updated_at: string;
  created_by: number | null;
  updated_by: number | null;
}

export interface FormSubmission {
  id: number;
  form: Form;
  fieldsResponse: FormFieldResponse[];
  status: string;
  created_at: string;
  updated_at: string;
  project: number;
  approve_by: number | null;
  created_by: number;
  updated_by: number;
}


export interface Form {
  id: number;
  subjects: number[];
  title: string;
  description: string;
  main: number | null;
  starttime: Date;
  endtime: Date;
  created_at: string;
  updated_at: string;
  created_by: number | null;
  updated_by: number | null;
}

export interface Project {
  id: number;
  title_th: string;
  title_en: string;
  keyword: string[];
  subject: SubjectResponse;
  student: UserResponse;
  created_by: number | null;
  created_at: string;
  updated_at: string;
  updated_by: number | null;
}
export interface AssignmentTeacherResponse {
  id: number;
  form: Form;
  project: CreateProjectResponse;
  status: "Pending" | "Approved" | "Rejected";
  created_at: string;
  updated_at: string;
  approve_by: number | null;
  created_by: number;
  updated_by: number;
}