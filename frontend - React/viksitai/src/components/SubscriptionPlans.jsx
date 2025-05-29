
import React, { useState, useEffect } from 'react';

const SubscriptionPlans = ({ onGoogleSignIn, onClose }) => {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-70">
      <div className="max-w-4xl transform overflow-hidden rounded-xl bg-gray-800 p-6 shadow-2xl transition-all duration-300 sm:p-8">
        <h2 className="mb-6 text-center text-2xl font-bold text-white">Choose Your Plan</h2>
        
        <div className="grid gap-8 md:grid-cols-3">
          {/* Free Plan */}
          <div className="group relative overflow-hidden rounded-lg bg-gradient-to-br from-gray-700 to-gray-900 p-6 shadow-lg transition-all duration-300 hover:shadow-blue-500/20">
            <div className="absolute -right-4 -top-4 h-24 w-24 rounded-full bg-blue-500 opacity-20 blur-xl transition-all duration-300 group-hover:opacity-30"></div>
            <h3 className="mb-4 text-xl font-bold text-white">Free</h3>
            <p className="mb-2 text-3xl font-bold text-white">$0<span className="text-sm font-normal text-gray-400">/month</span></p>
            <ul className="mb-6 space-y-2 text-gray-300">
              <li className="flex items-center">
                <svg className="mr-2 h-5 w-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Basic code explanations
              </li>
              <li className="flex items-center">
                <svg className="mr-2 h-5 w-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Limited repositories
              </li>
              <li className="flex items-center">
                <svg className="mr-2 h-5 w-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Community support
              </li>
            </ul>
            <button 
              onClick={onGoogleSignIn}
              className="w-full rounded-lg bg-blue-600 py-2 font-medium text-white transition-colors hover:bg-blue-700"
            >
              Get Started
            </button>
          </div>
          
          {/* Pro Plan */}
          <div className="group relative overflow-hidden rounded-lg bg-gradient-to-br from-blue-900 to-indigo-900 p-6 shadow-lg transition-all duration-300 hover:shadow-indigo-500/30">
            <div className="absolute -right-4 -top-4 h-32 w-32 rounded-full bg-indigo-500 opacity-20 blur-xl transition-all duration-300 group-hover:opacity-40"></div>
            <span className="absolute -right-1 -top-1 rounded-bl-lg bg-indigo-600 px-3 py-1 text-xs font-medium text-white">Popular</span>
            <h3 className="mb-4 text-xl font-bold text-white">Pro</h3>
            <p className="mb-2 text-3xl font-bold text-white">$9.99<span className="text-sm font-normal text-gray-300">/month</span></p>
            <ul className="mb-6 space-y-2 text-gray-200">
              <li className="flex items-center">
                <svg className="mr-2 h-5 w-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Advanced code analysis
              </li>
              <li className="flex items-center">
                <svg className="mr-2 h-5 w-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Unlimited repositories
              </li>
              <li className="flex items-center">
                <svg className="mr-2 h-5 w-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Priority support
              </li>
              <li className="flex items-center">
                <svg className="mr-2 h-5 w-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Documentation generation
              </li>
            </ul>
            <button 
              className="w-full rounded-lg bg-indigo-600 py-2 font-medium text-white transition-colors hover:bg-indigo-700"
            >
              Sign Up Now
            </button>
          </div>
          
          {/* Enterprise Plan */}
          <div className="group relative overflow-hidden rounded-lg bg-gradient-to-br from-gray-700 to-gray-900 p-6 shadow-lg transition-all duration-300 hover:shadow-purple-500/20">
            <div className="absolute -right-4 -top-4 h-24 w-24 rounded-full bg-purple-500 opacity-20 blur-xl transition-all duration-300 group-hover:opacity-30"></div>
            <h3 className="mb-4 text-xl font-bold text-white">Enterprise</h3>
            <p className="mb-2 text-3xl font-bold text-white">$24.99<span className="text-sm font-normal text-gray-400">/month</span></p>
            <ul className="mb-6 space-y-2 text-gray-300">
              <li className="flex items-center">
                <svg className="mr-2 h-5 w-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Everything in Pro
              </li>
              <li className="flex items-center">
                <svg className="mr-2 h-5 w-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Team collaboration
              </li>
              <li className="flex items-center">
                <svg className="mr-2 h-5 w-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Dedicated support
              </li>
              <li className="flex items-center">
                <svg className="mr-2 h-5 w-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Custom integrations
              </li>
            </ul>
            <button 
              
              className="w-full rounded-lg bg-purple-600 py-2 font-medium text-white transition-colors hover:bg-purple-700"
            >
              Contact Sales
            </button>
          </div>
        </div>
        
        <div className="mt-8 text-center">
          <button 
            className="text-sm text-gray-400 underline hover:text-white"
            onClick={onClose}
          >
            No thanks, continue with free trial
          </button>
        </div>
      </div>
    </div>
  );
};

export default SubscriptionPlans;