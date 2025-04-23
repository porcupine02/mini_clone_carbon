// import { defineStore } from 'pinia';
// import { type permissions } from '~/types/cookies';

// const COOKIE_NAME = 'access_token';

// export const usePermissionStore = () => {
//   // Define store
//   const store = defineStore('permission', {
//     state: () => ({
//       permissions: [] as Array<string>,
//     }),
//     actions: {
//       async setPermissions(projectId?: number | string, orgId?: number | string) {
//         console.log('projectId', projectId)
//         console.log('orgId', orgId)
//         // (1) get all permission from token
//         const allPermissions = getDataFromTokenInCookie(
//           COOKIE_NAME,
//           'permissions',
//         ) as permissions[];
//         this.permissions = [];
//         if (allPermissions) {
//           // (2) loop : check which user select and pick all permission for use
//           if (!projectId && !orgId) {
//             console.log('1')
//             console.log('projectId', projectId)
//             console.log('orgId', orgId)
//             // intersec start
//             let filterPermission: string[][] = allPermissions.map(value => value.permission);
//             if (filterPermission.length > 0) {
//               this.permissions = filterPermission.reduce(
//                 (acc, curr) => acc.filter(perm => curr.includes(perm)),
//                 [...filterPermission[0]]
//               );
//             }
//               //  intersec end
//           } else {
//             const system: string[] = [];
//             const project: string[] = [];
//             const org: string[] = [];

//             allPermissions.forEach((value) => {
//               if (value.level === 'SYSTEM') {
//                 console.log('A')
//                 system.push(...value.permission);
//               } else if (value.level === 'PROJECT' && value.project_id === projectId) {
//                 console.log('B')
//                 project.push(...value.permission);
//               } else if (value.level === 'ORGANIZATION' && value.org_id === orgId) {
//                 console.log('C')
//                 org.push(...value.permission);
//               }
//             });

//             if (projectId && !orgId) {
//               if (project.length > 0) {
//                 this.permissions = [...project];
//               } else {
//                 this.permissions = [...system];
//               }
//             } else if (projectId && orgId) {
//               if (org.length > 0) {
//                 this.permissions = [...org];
//               } else if (project.length > 0) {
//                 this.permissions = [...project];
//               } else {
//                 this.permissions = [...system];
//               }
//             }
//           }
//         }

//         console.log('permission : ', this.permissions);
//       },

//       /**
//        *
//        * @param permissionName string[] - Array of permission names
//        * @param options 'all' | 'some' Default is 'all' - Check if all or some permissions are in the permissions array
//        * @returns boolean
//        */

//       checkPermission(permissionName: string[], option: 'all' | 'some' = 'all'): boolean {
//         // Check if all or some permissions are in the permissions array

//         // Parse option to arrayOption all = Array.every, some = Array.some. And Default is 'every'
//         const arrayOption = option === 'all' ? 'every' : 'some';

//         return permissionName[arrayOption]((permission: string) =>
//           this.permissions.includes(permission),
//         );
//       },
//     },
//     getters: {
//       getPermissions(): string[] | [] {
//         return this.permissions;
//       },
//     },
//   });

//   // Initialize store
//   const permissionStore = store() as any;
//   // const xchStore = useXchStore();
//   // Get permissions from token and store it to the store
//   const decodedToken = getDataFromTokenInCookie(COOKIE_NAME, 'permissions');
//   // permissionStore.setPermissions(decodedToken || []);
  
//   permissionStore.setPermissions();

//   return permissionStore;
// };
