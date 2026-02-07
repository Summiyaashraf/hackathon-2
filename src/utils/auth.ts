// Authentication utilities for managing JWT tokens

const TOKEN_KEY = 'better-auth-token';

/**
 * Store the authentication token in localStorage
 */
export function setAuthToken(token: string): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem(TOKEN_KEY, token);
  }
}

/**
 * Retrieve the authentication token from localStorage
 */
export function getAuthToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem(TOKEN_KEY);
  }
  return null;
}

/**
 * Remove the authentication token from localStorage
 */
export function removeAuthToken(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(TOKEN_KEY);
  }
}

/**
 * Check if the user is currently authenticated
 */
export function isAuthenticated(): boolean {
  const token = getAuthToken();
  if (!token) {
    return false;
  }

  // Check if token is expired
  try {
    const payload = parseJwtPayload(token);
    const currentTime = Math.floor(Date.now() / 1000);

    // Return true if token is not expired
    return payload.exp > currentTime;
  } catch {
    // If there's an error parsing the token, assume it's invalid
    return false;
  }
}

/**
 * Parse JWT payload to extract user information
 */
export function parseJwtPayload(token: string): { sub: string; email: string; exp: number; iat: number } {
  const parts = token.split('.');
  if (parts.length !== 3) {
    throw new Error('Invalid token format');
  }

  const payload = parts[1];
  // Replace URL-safe base64 characters back to standard base64
  let base64 = payload.replace(/-/g, '+').replace(/_/g, '/');
  // Add padding if needed
  const pad = base64.length % 4;
  if (pad) {
    base64 = payload.replace(/-/g, '+').replace(/_/g, '/');
  }

  const decodedPayload = atob(base64);
  return JSON.parse(decodedPayload);
}

/**
 * Get user ID from token
 */
export function getUserIdFromToken(): string | null {
  const token = getAuthToken();
  if (!token) {
    return null;
  }

  try {
    const payload = parseJwtPayload(token);
    return payload.sub; // 'sub' typically contains the user ID
  } catch (error) {
    console.error('Error getting user ID from token:', error);
    return null;
  }
}

/**
 * Get email from token
 */
export function getUserEmailFromToken(): string | null {
  const token = getAuthToken();
  if (!token) {
    return null;
  }

  try {
    const payload = parseJwtPayload(token);
    return payload.email;
  } catch (error) {
    console.error('Error getting user email from token:', error);
    return null;
  }
}