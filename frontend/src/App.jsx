import React, { useState, useEffect, useRef } from 'react';
import {
  FileText,
  UploadCloud,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Download,
  Sparkles,
  BookOpen,
  BarChart3,
  Layers,
  ArrowRight,
  RefreshCw,
  ExternalLink,
  Clock,
  Briefcase,
  Sliders,
  Check,
  Search
} from 'lucide-react';

export default function App() {
  // Input states
  const [resumeText, setResumeText] = useState('');
  const [resumeFileName, setResumeFileName] = useState('');
  const [jdText, setJdText] = useState('');
  const [skillWeight, setSkillWeight] = useState(0.60);
  const [activeTab, setActiveTab] = useState('skills');

  // Loading & Status
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [apiConnected, setApiConnected] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [results, setResults] = useState(null);
  const [samples, setSamples] = useState({});
  const [tableSearch, setTableSearch] = useState('');

  const fileInputRef = useRef(null);

  // Check backend health & fetch samples on load
  useEffect(() => {
    fetch('/api/health')
      .then(res => res.json())
      .then(data => {
        if (data.status === 'ok') setApiConnected(true);
      })
      .catch(() => setApiConnected(false));

    fetch('/api/samples')
      .then(res => res.json())
      .then(data => setSamples(data))
      .catch(err => console.error('Error fetching samples:', err));
  }, []);

  // Handle PDF file upload
  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setErrorMessage('Please upload a valid PDF document.');
      return;
    }

    setErrorMessage('');
    setIsUploading(true);
    setResumeFileName(file.name);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/upload-resume', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'PDF processing failed');
      }

      const data = await response.json();
      setResumeText(data.text);
    } catch (err) {
      setErrorMessage(err.message || 'Failed to parse PDF.');
    } finally {
      setIsUploading(false);
    }
  };

  // Load sample data
  const loadSample = (type) => {
    setErrorMessage('');
    if (type === 'data_analyst') {
      setResumeText(samples.data_analyst_resume || '');
      setJdText(samples.data_analyst_jd || '');
      setResumeFileName('sample_resume_data_analyst.pdf');
    } else if (type === 'software_engineer') {
      setResumeText(samples.software_engineer_resume || '');
      setJdText(samples.software_engineer_jd || '');
      setResumeFileName('sample_resume_software_engineer.pdf');
    }
    setResults(null);
  };

  // Clear inputs
  const handleClear = () => {
    setResumeText('');
    setResumeFileName('');
    setJdText('');
    setResults(null);
    setErrorMessage('');
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  // Perform Matching Analysis
  const handleAnalyze = async () => {
    if (!resumeText.trim()) {
      setErrorMessage('Please upload a resume or paste resume text.');
      return;
    }
    if (!jdText.trim()) {
      setErrorMessage('Please paste the target job description.');
      return;
    }

    setErrorMessage('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/match', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_text: resumeText,
          jd_text: jdText,
          skill_weight: skillWeight,
          text_weight: Number((1.0 - skillWeight).toFixed(2)),
          candidate_name: resumeFileName || 'Applicant',
          job_title: 'Target Role',
        }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Matching failed');
      }

      const data = await response.json();
      setResults(data);
      // Auto-scroll to results
      setTimeout(() => {
        document.getElementById('results-section')?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } catch (err) {
      setErrorMessage(err.message || 'Analysis encountered an error.');
    } finally {
      setIsLoading(false);
    }
  };

  // Download CSV report
  const handleDownloadCsv = async () => {
    try {
      const response = await fetch('/api/export-csv', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_text: resumeText,
          jd_text: jdText,
          skill_weight: skillWeight,
          text_weight: Number((1.0 - skillWeight).toFixed(2)),
        }),
      });
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'resume_job_match_report.csv';
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (err) {
      console.error('Failed to download CSV:', err);
    }
  };

  // Download Markdown summary
  const handleDownloadMarkdown = () => {
    if (!results?.exec_summary) return;
    const blob = new Blob([results.exec_summary], { type: 'text/markdown' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'resume_match_executive_summary.md';
    document.body.appendChild(a);
    a.click();
    a.remove();
  };

  const matchData = results?.match_results;
  const overallScore = matchData ? matchData.overall_score : 0;

  // Status badge styling helper
  const getScoreStatus = (score) => {
    if (score >= 75) return { label: 'Strong Fit', color: 'text-emerald-700 bg-emerald-50 border-emerald-200' };
    if (score >= 50) return { label: 'Moderate Fit', color: 'text-amber-700 bg-amber-50 border-amber-200' };
    return { label: 'Needs Upskilling', color: 'text-rose-700 bg-rose-50 border-rose-200' };
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Navigation Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-blue-600 text-white flex items-center justify-center shadow-md shadow-blue-500/20 font-bold text-lg">
              📄
            </div>
            <div>
              <h1 className="text-lg font-bold text-slate-900 leading-tight">AI Resume Analyzer</h1>
              <p className="text-xs text-slate-500">TF-IDF & NLP Job Matching Engine</p>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            {/* Status indicator */}
            <div className="flex items-center space-x-2 text-xs font-medium px-3 py-1.5 rounded-full bg-slate-100 border border-slate-200">
              <span className={`w-2 h-2 rounded-full ${apiConnected ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`} />
              <span className="text-slate-600">{apiConnected ? 'API Connected' : 'Connecting to API...'}</span>
            </div>

            <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-blue-50 text-blue-700 border border-blue-200">
              React + FastAPI
            </span>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full">
        {/* Hero Section */}
        <div className="bg-gradient-to-r from-blue-900 via-blue-800 to-indigo-900 text-white rounded-2xl p-6 sm:p-8 shadow-xl shadow-blue-950/10 mb-8 relative overflow-hidden">
          <div className="relative z-10 max-w-3xl">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-white/10 backdrop-blur-md text-xs font-semibold text-blue-200 mb-3 border border-white/15">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Offline Privacy-First NLP & Skill Taxonomy</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight mb-2">
              Optimize Your Job Alignment & Bridge Skill Gaps
            </h2>
            <p className="text-blue-100 text-sm sm:text-base leading-relaxed">
              Upload your PDF resume and paste target job requirements. The application extracts technical skills,
              calculates skill coverage & TF-IDF similarity, discovers missing competencies, and maps personalized learning roadmaps.
            </p>
          </div>
          {/* Subtle background glow */}
          <div className="absolute -right-12 -bottom-12 w-64 h-64 bg-blue-500/20 rounded-full blur-3xl pointer-events-none" />
        </div>

        {/* Error Alert */}
        {errorMessage && (
          <div className="mb-6 p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 flex items-start space-x-3 text-sm">
            <AlertTriangle className="w-5 h-5 flex-shrink-0 mt-0.5 text-rose-600" />
            <div>
              <p className="font-semibold">Notice</p>
              <p>{errorMessage}</p>
            </div>
          </div>
        )}

        {/* Preset Sample Bar */}
        <div className="bg-white rounded-xl border border-slate-200 p-4 mb-6 shadow-sm flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center space-x-2 text-xs font-medium text-slate-500">
            <Briefcase className="w-4 h-4 text-slate-400" />
            <span>Load Preloaded Demo:</span>
          </div>

          <div className="flex items-center flex-wrap gap-2">
            <button
              onClick={() => loadSample('data_analyst')}
              className="text-xs font-semibold px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-blue-50 hover:text-blue-700 text-slate-700 border border-slate-200 transition-colors"
            >
              📊 Data Analyst Demo
            </button>
            <button
              onClick={() => loadSample('software_engineer')}
              className="text-xs font-semibold px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-blue-50 hover:text-blue-700 text-slate-700 border border-slate-200 transition-colors"
            >
              💻 Software Engineer Demo
            </button>
            <button
              onClick={handleClear}
              className="text-xs font-semibold px-3 py-1.5 rounded-lg bg-slate-50 hover:bg-slate-100 text-slate-500 border border-slate-200 transition-colors"
            >
              Clear
            </button>
          </div>
        </div>

        {/* Two-Column Input Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Column 1: Resume Upload */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <FileText className="w-5 h-5 text-blue-600" />
                <h3 className="font-bold text-slate-800">1. Resume Input (PDF)</h3>
              </div>
              {resumeFileName && (
                <span className="text-xs font-medium px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-600 truncate max-w-[200px]">
                  {resumeFileName}
                </span>
              )}
            </div>

            {/* Drag & Drop Upload Zone */}
            <div
              onClick={() => fileInputRef.current?.click()}
              className={`border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all duration-200 mb-4 ${
                isUploading
                  ? 'border-blue-400 bg-blue-50/50'
                  : 'border-slate-300 hover:border-blue-500 hover:bg-slate-50/70'
              }`}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                className="hidden"
                onChange={handleFileUpload}
              />
              <UploadCloud className="w-10 h-10 mx-auto text-blue-500 mb-2 stroke-[1.5]" />
              <p className="text-sm font-semibold text-slate-800">
                {isUploading ? 'Extracting text with PyMuPDF...' : 'Click to upload resume (PDF)'}
              </p>
              <p className="text-xs text-slate-400 mt-1">
                Standard single/multi-page PDF resumes up to 10MB
              </p>
            </div>

            {/* Resume Text Editor / Preview */}
            <div className="flex-1 flex flex-col">
              <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
                Extracted Resume Text Preview
              </label>
              <textarea
                value={resumeText}
                onChange={(e) => setResumeText(e.target.value)}
                placeholder="Extracted resume text appears here automatically, or you can paste text directly..."
                className="w-full flex-1 min-h-[220px] p-3 text-xs leading-relaxed font-mono bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none resize-y"
              />
              <div className="flex justify-between items-center text-xs text-slate-400 mt-2">
                <span>Words: {resumeText.trim() ? resumeText.trim().split(/\s+/).length : 0}</span>
                <span>Characters: {resumeText.length}</span>
              </div>
            </div>
          </div>

          {/* Column 2: Job Description */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <Briefcase className="w-5 h-5 text-indigo-600" />
                <h3 className="font-bold text-slate-800">2. Target Job Description</h3>
              </div>
              <span className="text-xs text-slate-400">Paste Posting</span>
            </div>

            <div className="flex-1 flex flex-col">
              <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
                Requirements & Responsibilities
              </label>
              <textarea
                value={jdText}
                onChange={(e) => setJdText(e.target.value)}
                placeholder="Paste the target job description, requirements, qualification bullets, or role expectations here..."
                className="w-full flex-1 min-h-[350px] p-3 text-xs leading-relaxed bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none resize-y"
              />
              <div className="flex justify-between items-center text-xs text-slate-400 mt-2">
                <span>Words: {jdText.trim() ? jdText.trim().split(/\s+/).length : 0}</span>
                <span>Characters: {jdText.length}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Configuration Bar & Run Button */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm mb-8 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center space-x-4 w-full md:w-auto">
            <Sliders className="w-5 h-5 text-slate-400 flex-shrink-0" />
            <div className="flex-1 md:w-80">
              <div className="flex justify-between text-xs font-medium text-slate-600 mb-1">
                <span>Skill Match Weight: <b>{Math.round(skillWeight * 100)}%</b></span>
                <span>Text Similarity: <b>{Math.round((1 - skillWeight) * 100)}%</b></span>
              </div>
              <input
                type="range"
                min="0.2"
                max="0.8"
                step="0.05"
                value={skillWeight}
                onChange={(e) => setSkillWeight(parseFloat(e.target.value))}
                className="w-full accent-blue-600 h-1.5 bg-slate-200 rounded-lg cursor-pointer"
              />
            </div>
          </div>

          <button
            onClick={handleAnalyze}
            disabled={isLoading || isUploading}
            className={`w-full md:w-auto px-8 py-3 rounded-xl font-bold text-sm text-white shadow-md transition-all flex items-center justify-center space-x-2 ${
              isLoading
                ? 'bg-blue-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700 shadow-blue-500/25 active:scale-[0.98]'
            }`}
          >
            {isLoading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Computing TF-IDF & Skills...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Analyze & Match Resume</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>

        {/* RESULTS SECTION */}
        {results && matchData && (
          <div id="results-section" className="space-y-6 pt-4">
            {/* KPI Metrics Row */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Overall Score */}
              <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
                <div className="flex justify-between items-start mb-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Overall Match</span>
                  <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${getScoreStatus(overallScore).color}`}>
                    {getScoreStatus(overallScore).label}
                  </span>
                </div>
                <div className="text-3xl font-extrabold text-slate-900 mb-1">
                  {overallScore.toFixed(1)}%
                </div>
                {/* Progress bar */}
                <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden mt-3">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${
                      overallScore >= 75 ? 'bg-emerald-500' : overallScore >= 50 ? 'bg-amber-500' : 'bg-rose-500'
                    }`}
                    style={{ width: `${overallScore}%` }}
                  />
                </div>
              </div>

              {/* Skill Coverage Score */}
              <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
                <div className="flex justify-between items-start mb-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Skill Coverage</span>
                  <span className="text-xs text-blue-600 font-semibold bg-blue-50 px-2 py-0.5 rounded-full border border-blue-200">
                    Exact Matches
                  </span>
                </div>
                <div className="text-3xl font-extrabold text-blue-600 mb-1">
                  {matchData.skill_coverage_score.toFixed(1)}%
                </div>
                <p className="text-xs text-slate-500 mt-2">
                  Matched <b>{matchData.matched_skills.length}</b> of <b>{matchData.total_jd_skills}</b> required skills
                </p>
              </div>

              {/* TF-IDF Similarity Score */}
              <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
                <div className="flex justify-between items-start mb-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Text Similarity</span>
                  <span className="text-xs text-purple-600 font-semibold bg-purple-50 px-2 py-0.5 rounded-full border border-purple-200">
                    TF-IDF Cosine
                  </span>
                </div>
                <div className="text-3xl font-extrabold text-purple-600 mb-1">
                  {matchData.text_similarity_score.toFixed(1)}%
                </div>
                <p className="text-xs text-slate-500 mt-2">
                  Contextual n-gram lexical overlap
                </p>
              </div>

              {/* Skill Gaps Count */}
              <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
                <div className="flex justify-between items-start mb-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Skill Gaps</span>
                  <span className="text-xs text-rose-600 font-semibold bg-rose-50 px-2 py-0.5 rounded-full border border-rose-200">
                    Gaps
                  </span>
                </div>
                <div className="text-3xl font-extrabold text-rose-600 mb-1">
                  {matchData.missing_skills.length}
                </div>
                <p className="text-xs text-slate-500 mt-2">
                  Targeted competencies to acquire
                </p>
              </div>
            </div>

            {/* Action Bar / Download Toolbar */}
            <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm flex flex-wrap items-center justify-between gap-4">
              <div className="text-xs font-medium text-slate-600">
                Analysis complete for <b>{resumeFileName || 'Resume'}</b> against target specifications.
              </div>
              <div className="flex items-center space-x-3">
                <button
                  onClick={handleDownloadCsv}
                  className="px-4 py-2 rounded-xl text-xs font-bold bg-slate-900 hover:bg-slate-800 text-white flex items-center space-x-2 transition-all shadow-sm"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Download CSV Report</span>
                </button>
                <button
                  onClick={handleDownloadMarkdown}
                  className="px-4 py-2 rounded-xl text-xs font-bold bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200 flex items-center space-x-2 transition-all"
                >
                  <FileText className="w-3.5 h-3.5" />
                  <span>Executive Summary (.md)</span>
                </button>
              </div>
            </div>

            {/* Tabs Container */}
            <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
              {/* Tab Header */}
              <div className="border-b border-slate-200 px-6 flex space-x-8">
                <button
                  onClick={() => setActiveTab('skills')}
                  className={`py-4 text-sm font-bold border-b-2 transition-all flex items-center space-x-2 ${
                    activeTab === 'skills'
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-slate-500 hover:text-slate-700'
                  }`}
                >
                  <Layers className="w-4 h-4" />
                  <span>Skills Breakdown</span>
                  <span className="text-xs bg-slate-100 px-2 py-0.5 rounded-full text-slate-600">
                    {matchData.matched_skills.length + matchData.missing_skills.length}
                  </span>
                </button>

                <button
                  onClick={() => setActiveTab('recs')}
                  className={`py-4 text-sm font-bold border-b-2 transition-all flex items-center space-x-2 ${
                    activeTab === 'recs'
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-slate-500 hover:text-slate-700'
                  }`}
                >
                  <BookOpen className="w-4 h-4" />
                  <span>Learning Pathways</span>
                  <span className="text-xs bg-rose-100 px-2 py-0.5 rounded-full text-rose-700">
                    {results.recommendations.length}
                  </span>
                </button>

                <button
                  onClick={() => setActiveTab('table')}
                  className={`py-4 text-sm font-bold border-b-2 transition-all flex items-center space-x-2 ${
                    activeTab === 'table'
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-slate-500 hover:text-slate-700'
                  }`}
                >
                  <BarChart3 className="w-4 h-4" />
                  <span>Comparison Table</span>
                </button>

                <button
                  onClick={() => setActiveTab('domain')}
                  className={`py-4 text-sm font-bold border-b-2 transition-all flex items-center space-x-2 ${
                    activeTab === 'domain'
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-slate-500 hover:text-slate-700'
                  }`}
                >
                  <Briefcase className="w-4 h-4" />
                  <span>Domain Analytics</span>
                </button>
              </div>

              {/* Tab Content */}
              <div className="p-6">
                {/* TAB 1: Skills Breakdown */}
                {activeTab === 'skills' && (
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Matched Skills */}
                    <div className="rounded-xl border border-emerald-200 bg-emerald-50/30 p-5">
                      <div className="flex items-center space-x-2 mb-3">
                        <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                        <h4 className="font-bold text-emerald-950 text-sm">
                          Matched Skills ({matchData.matched_skills.length})
                        </h4>
                      </div>
                      <p className="text-xs text-slate-500 mb-4">
                        Competencies verified in both your resume and the posting:
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {matchData.matched_skills.map((skill) => (
                          <span
                            key={skill}
                            className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100/80 text-emerald-800 border border-emerald-300"
                          >
                            <Check className="w-3 h-3 stroke-[2.5]" />
                            <span>{skill}</span>
                          </span>
                        ))}
                        {matchData.matched_skills.length === 0 && (
                          <span className="text-xs text-slate-400 italic">No matching skills detected.</span>
                        )}
                      </div>
                    </div>

                    {/* Missing Skills */}
                    <div className="rounded-xl border border-rose-200 bg-rose-50/30 p-5">
                      <div className="flex items-center space-x-2 mb-3">
                        <XCircle className="w-5 h-5 text-rose-600" />
                        <h4 className="font-bold text-rose-950 text-sm">
                          Missing Skills ({matchData.missing_skills.length})
                        </h4>
                      </div>
                      <p className="text-xs text-slate-500 mb-4">
                        Explicit job requirements not found in your resume:
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {matchData.missing_skills.map((skill) => (
                          <span
                            key={skill}
                            className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-rose-100/80 text-rose-800 border border-rose-300"
                          >
                            <span>✗ {skill}</span>
                          </span>
                        ))}
                        {matchData.missing_skills.length === 0 && (
                          <span className="text-xs text-emerald-700 font-semibold">
                            🎉 100% hard skill coverage!
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Additional Skills */}
                    <div className="rounded-xl border border-blue-200 bg-blue-50/30 p-5">
                      <div className="flex items-center space-x-2 mb-3">
                        <Sparkles className="w-5 h-5 text-blue-600" />
                        <h4 className="font-bold text-blue-950 text-sm">
                          Candidate Strengths ({matchData.extra_skills.length})
                        </h4>
                      </div>
                      <p className="text-xs text-slate-500 mb-4">
                        Bonus skills found in your resume beyond the stated requirements:
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {matchData.extra_skills.map((skill) => (
                          <span
                            key={skill}
                            className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-blue-100/80 text-blue-800 border border-blue-300"
                          >
                            <span>+ {skill}</span>
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {/* TAB 2: Learning Pathways */}
                {activeTab === 'recs' && (
                  <div className="space-y-4">
                    <div className="flex justify-between items-center mb-2">
                      <h4 className="text-sm font-bold text-slate-800">
                        Tailored Action Roadmaps for Missing Skills
                      </h4>
                      <span className="text-xs text-slate-500">
                        Official docs, tutorials, and project recommendations
                      </span>
                    </div>

                    {results.recommendations.length === 0 ? (
                      <div className="p-8 text-center text-emerald-700 font-semibold bg-emerald-50 rounded-xl border border-emerald-200">
                        🎉 You match all required skills! No immediate upskilling needed for this role.
                      </div>
                    ) : (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {results.recommendations.map((rec) => (
                          <div
                            key={rec.skill}
                            className="bg-white rounded-xl border border-slate-200 p-5 hover:border-blue-400 hover:shadow-md transition-all flex flex-col justify-between"
                          >
                            <div>
                              <div className="flex justify-between items-start mb-2">
                                <span className="font-bold text-slate-900 text-sm flex items-center space-x-1.5">
                                  <span>🎯 {rec.skill}</span>
                                </span>
                                <span className="text-xs font-medium px-2 py-0.5 rounded bg-slate-100 text-slate-600">
                                  {rec.category}
                                </span>
                              </div>

                              <a
                                href={rec.url}
                                target="_blank"
                                rel="noreferrer"
                                className="text-blue-600 hover:text-blue-800 font-semibold text-xs flex items-center space-x-1 mb-2 group"
                              >
                                <span className="group-hover:underline">{rec.title}</span>
                                <ExternalLink className="w-3.5 h-3.5 flex-shrink-0" />
                              </a>

                              <div className="flex items-center space-x-4 text-xs text-slate-500 mb-3">
                                <span>🏢 {rec.platform}</span>
                                <span className="flex items-center space-x-1">
                                  <Clock className="w-3 h-3 text-slate-400" />
                                  <span>{rec.estimated_time}</span>
                                </span>
                              </div>

                              <div className="bg-slate-50 rounded-lg p-3 text-xs text-slate-700 border border-slate-100 leading-relaxed">
                                <b className="text-slate-900 font-semibold">Suggested Action: </b>
                                {rec.action_plan}
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {/* TAB 3: Comparison Table */}
                {activeTab === 'table' && (
                  <div>
                    <div className="flex justify-between items-center mb-4">
                      <div className="relative w-72">
                        <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
                        <input
                          type="text"
                          value={tableSearch}
                          onChange={(e) => setTableSearch(e.target.value)}
                          placeholder="Search skills or status..."
                          className="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      </div>
                      <span className="text-xs text-slate-400">
                        Showing {results.table_records.filter(r => r.Skill.toLowerCase().includes(tableSearch.toLowerCase())).length} skills
                      </span>
                    </div>

                    <div className="overflow-x-auto border border-slate-200 rounded-xl">
                      <table className="w-full text-left text-xs">
                        <thead className="bg-slate-100/75 border-b border-slate-200 font-bold text-slate-600 uppercase tracking-wider">
                          <tr>
                            <th className="py-3 px-4">Skill</th>
                            <th className="py-3 px-4">Status</th>
                            <th className="py-3 px-4">Category</th>
                            <th className="py-3 px-4">Action Plan</th>
                            <th className="py-3 px-4">Resource</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-200 text-slate-700">
                          {results.table_records
                            .filter(r => r.Skill.toLowerCase().includes(tableSearch.toLowerCase()) || r.Status.toLowerCase().includes(tableSearch.toLowerCase()))
                            .map((row, idx) => (
                              <tr key={idx} className="hover:bg-slate-50/75 transition-colors">
                                <td className="py-3 px-4 font-bold text-slate-900">{row.Skill}</td>
                                <td className="py-3 px-4">
                                  <span
                                    className={`px-2 py-0.5 rounded-full text-[11px] font-semibold ${
                                      row.Status.startsWith('Matched')
                                        ? 'bg-emerald-100 text-emerald-800'
                                        : row.Status.startsWith('Missing')
                                        ? 'bg-rose-100 text-rose-800'
                                        : 'bg-blue-100 text-blue-800'
                                    }`}
                                  >
                                    {row.Status.split('(')[0]}
                                  </span>
                                </td>
                                <td className="py-3 px-4 text-slate-500">{row.Category}</td>
                                <td className="py-3 px-4 max-w-xs truncate">{row['Action / Recommendation']}</td>
                                <td className="py-3 px-4">
                                  {row['Learning Resource'] && row['Learning Resource'] !== 'N/A' ? (
                                    <a
                                      href={row['Learning Resource']}
                                      target="_blank"
                                      rel="noreferrer"
                                      className="text-blue-600 hover:underline flex items-center space-x-1"
                                    >
                                      <span>Link</span>
                                      <ExternalLink className="w-3 h-3" />
                                    </a>
                                  ) : (
                                    <span className="text-slate-400">—</span>
                                  )}
                                </td>
                              </tr>
                            ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}

                {/* TAB 4: Domain Analytics */}
                {activeTab === 'domain' && (
                  <div>
                    <h4 className="text-sm font-bold text-slate-800 mb-4">
                      Categorical Alignment Across Technical Domains
                    </h4>

                    <div className="space-y-4 max-w-3xl">
                      {Object.entries(matchData.category_breakdown || {}).map(([cat, val]) => {
                        if (val.jd_required === 0 && val.matched === 0) return null;
                        const pct = val.jd_required > 0 ? Math.round((val.matched / val.jd_required) * 100) : 100;
                        return (
                          <div key={cat} className="bg-slate-50 rounded-xl p-4 border border-slate-200">
                            <div className="flex justify-between text-xs font-bold text-slate-800 mb-1">
                              <span>{cat}</span>
                              <span>{val.matched} / {val.jd_required} matched ({pct}%)</span>
                            </div>
                            <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden">
                              <div
                                className="bg-blue-600 h-full rounded-full transition-all duration-500"
                                style={{ width: `${pct}%` }}
                              />
                            </div>
                            <div className="flex space-x-4 text-[11px] text-slate-500 mt-2">
                              <span>Required: <b>{val.jd_required}</b></span>
                              <span>Matched: <b className="text-emerald-700">{val.matched}</b></span>
                              <span>Missing: <b className="text-rose-700">{val.missing}</b></span>
                              {val.extra > 0 && <span>Bonus: <b className="text-blue-700">{val.extra}</b></span>}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-500">
        <p>AI Resume Analyzer & Job Matcher • Built with Python, Streamlit, FastAPI, React & Tailwind CSS</p>
      </footer>
    </div>
  );
}
