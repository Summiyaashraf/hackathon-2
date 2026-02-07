import React from 'react';

interface TaskInputProps {
  onClick: () => void;
}

const TaskInput: React.FC<TaskInputProps> = ({ onClick }) => {
  return (
    <div className="bg-white rounded-xl shadow-sm p-6 mb-6 border border-gray-100">
      <h2 className="text-lg font-semibold mb-4 text-gray-800">Create New Task</h2>
      <button
        onClick={onClick}
        className="w-full py-3 border-2 border-dashed border-gray-300 rounded-lg text-gray-500 hover:border-blue-400 hover:text-blue-600 transition-colors flex items-center justify-center"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
        </svg>
        Click to create a new task
      </button>
    </div>
  );
};

export default TaskInput;