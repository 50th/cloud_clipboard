export interface UserInfo {
  id: number
  username: string
  email: string
  access: string
  refresh: string
}

export interface Clipboard {
  id: number
  title: string
  description: string
  permission: string
  permission_display: string
  created_at: string
  updated_at: string
  last_modified_user: string
}

export interface ClipboardList {
  count: number
  next: string
  previous: string
  results: Clipboard[]
}

export interface ClipboardDetail {
  id: number
  title: string
  description: string
  permission: string
  permission_display: string
  created_at: string
  updated_at: string
  last_modified_user: string
  content: string
}
