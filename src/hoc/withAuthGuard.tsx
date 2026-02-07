import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import { isAuthenticated } from '../utils/auth';

// Higher-Order Component to protect routes
const withAuthGuard = <P extends object>(WrappedComponent: React.ComponentType<P>) => {
  const AuthGuard = (props: P) => {
    const router = useRouter();
    const [loading, setLoading] = useState(true);

    useEffect(() => {
      // Check authentication on component mount
      const checkAuth = () => {
        if (!isAuthenticated()) {
          // Redirect to login if not authenticated
          router.push('/auth/login');
        } else {
          setLoading(false);
        }
      };

      checkAuth();
    }, [router]);

    // Show nothing while checking authentication
    if (loading) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      );
    }

    // Render the wrapped component if authenticated
    return <WrappedComponent {...props} />;
  };

  return AuthGuard;
};

export default withAuthGuard;