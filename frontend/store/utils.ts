import { create } from 'zustand'


const URL = "http://127.0.0.1:8000"
export const useUtilsStore = create((set) => ({
  isLoading: false,
  isSearching: false,
  setIsLoading : () => set((state: any) => ({ isLoading: !state.isLoading})),
  setIsSearching: (bool: boolean) => set((state: any) => ({ isSearching: bool }))
}));