import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { Home, Inbox, Clock, CheckCircle, LogOut } from 'lucide-react';

interface SidebarProps {
  onLogout: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ onLogout }) => {
  const router = useRouter();

  const isActive = (path: string) => router.pathname === path;

  return (
    <aside className="w-64 bg-white dark:bg-gray-800 shadow-lg h-full flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-gray-200 dark:border-gray-700">
        <h1 className="text-2xl font-bold text-gray-800 dark:text-gray-100">TodoApp</h1>
        <p className="text-sm text-gray-500 dark:text-gray-400">Stay organized</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          <li>
            <Link
              href="/dashboard"
              className={`flex items-center p-3 rounded-lg transition-colors ${
                isActive('/dashboard')
                  ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              <Home className="w-5 h-5 mr-3" />
              Dashboard
            </Link>
          </li>
          <li>
            <Link
              href="/dashboard"
              className={`flex items-center p-3 rounded-lg transition-colors ${
                router.query.filter === undefined && isActive('/dashboard')
                  ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              <Inbox className="w-5 h-5 mr-3" />
              Inbox
            </Link>
          </li>
          <li>
            <Link
              href="/dashboard?filter=pending"
              className={`flex items-center p-3 rounded-lg transition-colors ${
                router.query.filter === 'pending'
                  ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              <Clock className="w-5 h-5 mr-3" />
              Today
            </Link>
          </li>
          <li>
            <Link
              href="/dashboard?filter=completed"
              className={`flex items-center p-3 rounded-lg transition-colors ${
                router.query.filter === 'completed'
                  ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              <CheckCircle className="w-5 h-5 mr-3" />
              Completed
            </Link>
          </li>
        </ul>
      </nav>

      {/* Logout */}
      <div className="p-4 border-t border-gray-200 dark:border-gray-700 mt-auto">
        <button
          onClick={onLogout}
          className="w-full flex items-center justify-center p-3 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
        >
          <LogOut className="w-5 h-5 mr-3" />
          Logout
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;