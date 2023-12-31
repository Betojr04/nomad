import React, { Suspense, lazy } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ErrorBoundary } from "react-error-boundary";

// Component Imports
import { Navbar } from "../components/Navbar.js";
import { Footer } from "../components/Footer.js";

// Lazy-Loaded components
// Ensure Register has a default export and the path is correct
const Register = lazy(() => import("./Register.js"));

export const Layout = () => {
  return (
    <Router>
      <Navbar />
      <ErrorBoundary FallbackComponent={() => <div>An error occurred!</div>}>
        <Suspense fallback={<div>Loading Your Page...</div>}>
          <Routes>
            <Route path="/" element={<Register />} />
            {/* Add more routes here */}
          </Routes>
        </Suspense>
      </ErrorBoundary>
      <Footer />
    </Router>
  );
};
