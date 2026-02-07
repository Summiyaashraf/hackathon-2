import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { Menu } from 'lucide-react';
import { isAuthenticated } from '../utils/auth';
import Sidebar from './Sidebar';
import Toast from './Toast';
import ThemeToggle from './ThemeToggle';

interface DashboardLayoutProps {
  children: React.ReactNode;
  onLogout: () => void;
  pageTitle?: string;
  errorMessage?: string | null;
  onClearError?: () => void;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({
  children,
  onLogout,
  pageTitle = 'Dashboard',
  errorMessage,
  onClearError
}) => {
  const router = useRouter();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Check if user is authenticated on component render
  useEffect(() => {
    const checkAuth = () => {
      if (!isAuthenticated()) {
        router.push('/auth/login'); // Redirect to login if not authenticated
      }
    };

    checkAuth();
  }, [router]);

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      {/* Mobile sidebar toggle */}
      <div className="lg:hidden fixed top-4 left-4 z-40">
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="p-2 rounded-md text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-800 shadow hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          <Menu className="h-6 w-6" />
        </button>
      </div>

      {/* Sidebar */}
      <div
        className={`fixed lg:static inset-y-0 left-0 z-30 w-64 bg-white dark:bg-gray-800 shadow-lg transform ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        } lg:translate-x-0 transition-transform duration-300 ease-in-out`}
      >
        <Sidebar onLogout={onLogout} />
      </div>

      {/* Overlay for mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-20 bg-black bg-opacity-50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        ></div>
      )}

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-white dark:bg-gray-800 shadow-sm z-10">
          <div className="flex items-center justify-between p-4">
            <div>
              <h1 className="text-xl font-semibold text-gray-800 dark:text-gray-100">{pageTitle}</h1>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-500 dark:text-gray-400 hidden sm:block">
                Welcome back!
              </div>
              <ThemeToggle />
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto p-4 md:p-6">
          {children}
        </main>
      </div>

      {/* Toast notifications */}
      {errorMessage && (
        <Toast
          message={errorMessage}
          type="error"
          onClose={onClearError || (() => {})}
        />
      )}
    </div>
  );
};

export default DashboardLayout;