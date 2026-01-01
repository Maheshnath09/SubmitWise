'use client';

import { GoogleOAuthProvider } from '@react-oauth/google';
import { ReactNode } from 'react';

const GOOGLE_CLIENT_ID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || '';

// Debug: Check if client ID is loaded
if (typeof window !== 'undefined') {
    console.log('Google Client ID loaded:', GOOGLE_CLIENT_ID ? 'Yes (length: ' + GOOGLE_CLIENT_ID.length + ')' : 'NO - MISSING!');
    if (!GOOGLE_CLIENT_ID) {
        console.error('NEXT_PUBLIC_GOOGLE_CLIENT_ID is not set! Add it to frontend/.env.local file');
    }
}

interface ProvidersProps {
    children: ReactNode;
}

export function Providers({ children }: ProvidersProps) {
    return (
        <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
            {children}
        </GoogleOAuthProvider>
    );
}

