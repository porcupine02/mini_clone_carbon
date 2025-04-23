export interface userLogin {
  username: string;
  email: string;
}
export interface responseLogin {
  refresh: string;
  access: string;
  user: userLogin;
  own_subject: number | null;
  own_project: number | null;
}

export interface formFields {
  id: string;
  label: string;
  type: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}
