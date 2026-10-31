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
  Search,
  ShieldCheck,
  Zap,
  Award,
  ChevronRight,
  TrendingUp,
  FileCheck,
  Flame,
  Code2
} from 'lucide-react';

export default function App() {
  // Input states
  const [resumeText, setResumeText] = useState('');
  const [resumeFileName, setResumeFileName] = useState('');
  const [resumeMeta, setResumeMeta] = useState(null);
  const [jdText, setJdText] = useState('');
  const [skillWeight, setSkillWeight] = useState(0.60);
  const [activeTab, setActiveTab] = useState('skills');
  const [inputMode, setInputMode] = useState('upload'); // 'upload' | 'text'

  // Loading & Status
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [apiConnected, setApiConnected] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [results, setResults] = useState(null);
  const [samples, setSamples] = useState({});
  const [tableSearch, setTableSearch] = useState('');
  const [isDragOver, setIsDragOver] = useState(false);

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
  const processFile = async (file) => {
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setErrorMessage('Please upload a valid PDF resume file.');
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
      setResumeMeta({
        wordCount: data.word_count,
        pages: data.num_pages,
        skillsCount: data.detected_skills?.length || 0
      });
    } catch (err) {
      setErrorMessage(err.message || 'Failed to parse PDF.');
    } finally {
      setIsUploading(false);
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files?.[0];
    if (file) processFile(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) processFile(file);
  };

  // Load sample data
  const loadSample = (type) => {
    setErrorMessage('');
    if (type === 'data_analyst') {
      setResumeText(samples.data_analyst_resume || '');
      setJdText(samples.data_analyst_jd || '');
      setResumeFileName('Alex_Turner_Data_Analyst.pdf');
      setResumeMeta({ wordCount: 284, pages: 1, skillsCount: 14 });
    } else if (type === 'software_engineer') {
      setResumeText(samples.software_engineer_resume || '');
      setJdText(samples.software_engineer_jd || '');
      setResumeFileName('Priya_Sharma_FullStack.pdf');
      setResumeMeta({ wordCount: 312, pages: 1, skillsCount: 16 });
    }
    setResults(null);
  };

  // Clear inputs
  const handleClear = () => {
    setResumeText('');
    setResumeFileName('');
    setResumeMeta(null);
    setJdText('');
    setResults(null);
    setErrorMessage('');
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  // Perform Matching Analysis
  const handleAnalyze = async () => {
    if (!resumeText.trim()) {
      setErrorMessage('Please upload a resume or paste resume text first.');
      return;
    }
    if (!jdText.trim()) {
      setErrorMessage('Please paste the target job description to match against.');
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
          job_title: 'Target Position',
        }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Matching calculation failed');
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
    if (score >= 75) return {
      label: 'Exceptional Fit',
      color: 'text-emerald-700 bg-emerald-500/10 border-emerald-400/40 ring-emerald-500/20',
      badge: 'bg-emerald-600',
      text: 'Your profile has high alignment with the core requirements of this role.'
    };
    if (score >= 50) return {
      label: 'Moderate Alignment',
      color: 'text-amber-700 bg-amber-500/10 border-amber-400/40 ring-amber-500/20',
      badge: 'bg-amber-600',
      text: 'Good foundational overlap with a few critical skill gaps to bridge.'
    };
    return {
      label: 'Needs Upskilling',
      color: 'text-rose-700 bg-rose-500/10 border-rose-400/40 ring-rose-500/20',
      badge: 'bg-rose-600',
      text: 'Multiple essential requirements are missing. Review recommendations below.'
    };
  };

  // SVG Circular Gauge calculation
  const circleRadius = 54;
  const circleCircumference = 2 * Math.PI * circleRadius;
  const strokeDashoffset = circleCircumference - (overallScore / 100) * circleCircumference;

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 via-slate-100/50 to-slate-50 text-slate-900 flex flex-col font-sans">
      {/* Top Navbar */}
      <header className="bg-white/80 backdrop-blur-md border-b border-slate-200/80 sticky top-0 z-40 transition-all">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-violet-600 text-white flex items-center justify-center shadow-md shadow-indigo-500/20 font-black text-lg">
              📄
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-extrabold text-slate-900 tracking-tight text-base sm:text-lg">
                  CareerMatch AI
                </span>
                <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200/60">
                  v1.2 Pro
                </span>
              </div>
              <p className="text-[11px] text-slate-500 hidden sm:block">AI Resume Analyzer & Gap Recommender</p>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            {/* Live API Health indicator */}
            <div className="flex items-center space-x-2 text-xs font-medium px-3 py-1.5 rounded-full bg-slate-100 border border-slate-200/80">
              <span className={`w-2 h-2 rounded-full ${apiConnected ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`} />
              <span className="text-slate-600 text-[11px] font-semibold">{apiConnected ? 'NLP Engine Active' : 'Connecting API...'}</span>
            </div>

            <a
              href="https://github.com/zakirsameerk6/Resume_Analyser"
              target="_blank"
              rel="noreferrer"
              className="text-xs font-semibold px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-white flex items-center space-x-1.5 transition-colors shadow-sm"
            >
              <span className="hidden sm:inline">Git-Repo</span>
            </a>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full">
        {/* Hero Banner */}
        <div className="relative rounded-3xl bg-gradient-to-br from-slate-900 via-indigo-950 to-blue-900 text-white p-7 sm:p-10 shadow-2xl shadow-indigo-950/20 mb-8 overflow-hidden border border-slate-800">
          <div className="relative z-10 max-w-3xl">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-white/10 backdrop-blur-md text-xs font-semibold text-indigo-200 mb-4 border border-white/15 shadow-inner">
              {/* <Sparkles className="w-3.5 h-3.5 text-amber-300" /> */}
              <span>Offline Privacy-First NLP & Skill Taxonomy</span>
            </div>
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight leading-tight mb-3">
              Know Exactly How Well Your Resume Matches Any Job.
            </h1>
            <p className="text-indigo-100/90 text-sm sm:text-base leading-relaxed mb-6 font-normal">
              Extract verified technical skills using <b>NLP tokenization</b>, calculate exact <b>TF-IDF Cosine Similarity</b>, identify missing competencies, and receive tailored project-based learning roadmaps.
            </p>

            {/* Quick feature tags */}
            <div className="flex flex-wrap items-center gap-3 text-xs text-indigo-200">
              <span className="flex items-center space-x-1.5 bg-white/5 px-2.5 py-1 rounded-lg border border-white/10">
                <Check className="w-3.5 h-3.5 text-emerald-400" />
                <span>60+ Tech Taxonomies</span>
              </span>
              <span className="flex items-center space-x-1.5 bg-white/5 px-2.5 py-1 rounded-lg border border-white/10">
                <ShieldCheck className="w-3.5 h-3.5 text-blue-400" />
                <span>100% Private (No External LLM)</span>
              </span>
              <span className="flex items-center space-x-1.5 bg-white/5 px-2.5 py-1 rounded-lg border border-white/10">
                <Zap className="w-3.5 h-3.5 text-amber-400" />
                <span>Sub-Second Analysis</span>
              </span>
            </div>
          </div>

          {/* Decorative glowing gradient orbs */}
          <div className="absolute -right-20 -bottom-20 w-80 h-80 bg-blue-500/25 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute right-40 -top-20 w-60 h-60 bg-indigo-500/20 rounded-full blur-3xl pointer-events-none" />
        </div>

        {/* Error Alert */}
        {errorMessage && (
          <div className="mb-6 p-4 rounded-2xl bg-rose-50 border border-rose-200/80 text-rose-800 flex items-start space-x-3 text-sm shadow-sm animate-fadeIn">
            <AlertTriangle className="w-5 h-5 flex-shrink-0 mt-0.5 text-rose-600" />
            <div>
              <p className="font-bold">Attention</p>
              <p>{errorMessage}</p>
            </div>
          </div>
        )}

        {/* 1-Click Interactive Demo Selector Bar */}
        {/* <div className="bg-white rounded-2xl border border-slate-200/80 p-4 mb-6 shadow-sm flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center space-x-2 text-xs font-semibold text-slate-600">
            <Flame className="w-4 h-4 text-amber-500 animate-pulse" />
            <span>Try 1-Click Sample Profiles:</span>
          </div>

          <div className="flex items-center flex-wrap gap-2.5">
            <button
              onClick={() => loadSample('data_analyst')}
              className="text-xs font-bold px-3.5 py-2 rounded-xl bg-gradient-to-r from-blue-50 to-indigo-50 hover:from-blue-100 hover:to-indigo-100 text-indigo-700 border border-indigo-200/70 transition-all flex items-center space-x-1.5 shadow-sm active:scale-95"
            >
              <span>📊 Senior Data Analyst</span>
              <span className="text-[10px] bg-indigo-200/60 px-1.5 py-0.2 rounded font-semibold">Alex</span>
            </button>
            <button
              onClick={() => loadSample('software_engineer')}
              className="text-xs font-bold px-3.5 py-2 rounded-xl bg-gradient-to-r from-purple-50 to-pink-50 hover:from-purple-100 hover:to-pink-100 text-purple-700 border border-purple-200/70 transition-all flex items-center space-x-1.5 shadow-sm active:scale-95"
            >
              <span>💻 Full-Stack Engineer</span>
              <span className="text-[10px] bg-purple-200/60 px-1.5 py-0.2 rounded font-semibold">Priya</span>
            </button>
            <button
              onClick={handleClear}
              className="text-xs font-semibold px-3 py-2 rounded-xl bg-slate-50 hover:bg-slate-100 text-slate-500 border border-slate-200 transition-colors"
            >
              Clear
            </button>
          </div>
        </div> */}

        {/* Two-Column Input Workspace */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Card 1: Resume Upload / Preview */}
          <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow">
            <div>
              {/* Header with Switcher */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center font-bold">
                    <FileText className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="font-bold text-slate-800 text-sm">Resume Input</h3>
                    <p className="text-[11px] text-slate-400">PDF document or direct text</p>
                  </div>
                </div>

                {/* Mode toggle */}
                <div className="flex bg-slate-100 p-0.5 rounded-lg text-xs font-semibold">
                  <button
                    onClick={() => setInputMode('upload')}
                    className={`px-2.5 py-1 rounded-md transition-all ${
                      inputMode === 'upload' ? 'bg-white shadow text-blue-700' : 'text-slate-500'
                    }`}
                  >
                    Dropzone
                  </button>
                  <button
                    onClick={() => setInputMode('text')}
                    className={`px-2.5 py-1 rounded-md transition-all ${
                      inputMode === 'text' ? 'bg-white shadow text-blue-700' : 'text-slate-500'
                    }`}
                  >
                    Edit Text
                  </button>
                </div>
              </div>

              {/* Upload Dropzone View */}
              {inputMode === 'upload' ? (
                <div>
                  <div
                    onClick={() => fileInputRef.current?.click()}
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-200 ${
                      isDragOver
                        ? 'border-blue-500 bg-blue-50 scale-[1.01]'
                        : 'border-slate-300 hover:border-blue-400 hover:bg-slate-50/60'
                    }`}
                  >
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept=".pdf"
                      className="hidden"
                      onChange={handleFileUpload}
                    />
                    <div className="w-14 h-14 mx-auto rounded-2xl bg-blue-50 border border-blue-100 flex items-center justify-center text-blue-600 mb-3 shadow-sm">
                      <UploadCloud className="w-7 h-7" />
                    </div>
                    <p className="text-sm font-bold text-slate-800">
                      {isUploading ? 'Extracting text via PyMuPDF...' : 'Drag & drop your PDF resume here'}
                    </p>
                    <p className="text-xs text-slate-400 mt-1">
                      or click to browse from your computer (PDF only)
                    </p>
                  </div>

                  {/* Uploaded File Meta Card */}
                  {resumeFileName && (
                    <div className="mt-4 p-3.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
                      <div className="flex items-center space-x-2.5 truncate max-w-xs">
                        <FileCheck className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                        <span className="font-semibold text-slate-700 truncate">{resumeFileName}</span>
                      </div>
                      {resumeMeta && (
                        <div className="flex items-center space-x-3 text-slate-500 font-medium">
                          <span>{resumeMeta.pages} page</span>
                          <span>•</span>
                          <span>{resumeMeta.wordCount} words</span>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ) : (
                /* Raw Text Edit View */
                <div>
                  <textarea
                    value={resumeText}
                    onChange={(e) => setResumeText(e.target.value)}
                    placeholder="Extracted resume text appears here automatically, or you can paste raw resume text..."
                    className="w-full min-h-[260px] p-3.5 text-xs font-mono leading-relaxed bg-slate-50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:outline-none resize-y"
                  />
                </div>
              )}
            </div>

            <div className="flex justify-between items-center text-xs text-slate-400 pt-3 border-t border-slate-100 mt-4">
              <span>Words: <b>{resumeText.trim() ? resumeText.trim().split(/\s+/).length : 0}</b></span>
              <span>Characters: <b>{resumeText.length}</b></span>
            </div>
          </div>

          {/* Card 2: Job Description Input */}
          <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow">
            <div>
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 rounded-lg bg-indigo-100 text-indigo-700 flex items-center justify-center font-bold">
                    <Briefcase className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="font-bold text-slate-800 text-sm">Target Job Description</h3>
                    <p className="text-[11px] text-slate-400">Paste role requirements & qualifications</p>
                  </div>
                </div>
                <span className="text-xs font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-600">
                  Target JD
                </span>
              </div>

              <textarea
                value={jdText}
                onChange={(e) => setJdText(e.target.value)}
                placeholder="Paste the target job description here (e.g. required skills, technologies, responsibilities, role expectations)..."
                className="w-full min-h-[260px] p-3.5 text-xs leading-relaxed bg-slate-50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:outline-none resize-y"
              />
            </div>

            <div className="flex justify-between items-center text-xs text-slate-400 pt-3 border-t border-slate-100 mt-4">
              <span>Words: <b>{jdText.trim() ? jdText.trim().split(/\s+/).length : 0}</b></span>
              <span>Characters: <b>{jdText.length}</b></span>
            </div>
          </div>
        </div>

        {/* Weights & Match Action Banner */}
        <div className="bg-white rounded-3xl border border-slate-200/80 p-5 shadow-sm mb-10 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center space-x-4 w-full md:w-auto">
            <div className="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center text-slate-500 flex-shrink-0">
              <Sliders className="w-5 h-5" />
            </div>
            <div className="flex-1 md:w-80">
              <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1.5">
                <span>Hard Skills: <b>{Math.round(skillWeight * 100)}%</b></span>
                <span>Contextual Similarity: <b>{Math.round((1 - skillWeight) * 100)}%</b></span>
              </div>
              <input
                type="range"
                min="0.2"
                max="0.8"
                step="0.05"
                value={skillWeight}
                onChange={(e) => setSkillWeight(parseFloat(e.target.value))}
                className="w-full accent-indigo-600 h-2 bg-slate-200 rounded-lg cursor-pointer"
              />
            </div>
          </div>

          <button
            onClick={handleAnalyze}
            disabled={isLoading || isUploading}
            className={`w-full md:w-auto px-8 py-4 rounded-2xl font-extrabold text-sm text-white shadow-xl transition-all flex items-center justify-center space-x-2.5 ${
              isLoading
                ? 'bg-indigo-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-600 via-indigo-600 to-violet-600 hover:from-blue-700 hover:to-violet-700 shadow-indigo-500/25 active:scale-95 hover:shadow-2xl hover:shadow-indigo-500/30'
            }`}
          >
            {isLoading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Extracting Skills & Computing Similarities...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4 text-amber-300" />
                <span>🚀 Analyze & Match Resume</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>

        {/* RESULTS DASHBOARD */}
        {results && matchData && (
          <div id="results-section" className="space-y-8 pt-2">
            {/* Main Score Hero Card */}
            <div className="bg-gradient-to-br from-white via-indigo-50/20 to-white rounded-3xl border border-indigo-100 p-6 sm:p-8 shadow-lg shadow-indigo-950/5 relative overflow-hidden">
              <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-center">
                {/* Radial Gauge */}
                <div className="md:col-span-4 flex flex-col items-center justify-center text-center">
                  <div className="relative w-40 h-40 flex items-center justify-center">
                    <svg className="w-full h-full transform -rotate-90" viewBox="0 0 128 128">
                      {/* Background circle */}
                      <circle
                        cx="64"
                        cy="64"
                        r={circleRadius}
                        className="stroke-slate-200/80"
                        strokeWidth="10"
                        fill="transparent"
                      />
                      {/* Animated Progress circle */}
                      <circle
                        cx="64"
                        cy="64"
                        r={circleRadius}
                        className={`transition-all duration-1000 ease-out ${
                          overallScore >= 75 ? 'stroke-emerald-500' : overallScore >= 50 ? 'stroke-amber-500' : 'stroke-rose-500'
                        }`}
                        strokeWidth="10"
                        strokeDasharray={circleCircumference}
                        strokeDashoffset={strokeDashoffset}
                        strokeLinecap="round"
                        fill="transparent"
                      />
                    </svg>

                    <div className="absolute flex flex-col items-center justify-center">
                      <span className="text-3xl font-black text-slate-900 tracking-tight">
                        {overallScore.toFixed(0)}%
                      </span>
                      <span className="text-[10px] uppercase font-bold text-slate-400 tracking-widest mt-0.5">
                        Match Index
                      </span>
                    </div>
                  </div>

                  {/* Status Badge */}
                  <div className={`mt-3 inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-bold border ring-1 ${getScoreStatus(overallScore).color}`}>
                    <Award className="w-3.5 h-3.5" />
                    <span>{getScoreStatus(overallScore).label}</span>
                  </div>
                </div>

                {/* Score Summary Metrics */}
                <div className="md:col-span-8 flex flex-col justify-center">
                  <h3 className="text-xl sm:text-2xl font-black text-slate-900 mb-1">
                    Candidate Compatibility Assessment
                  </h3>
                  <p className="text-xs sm:text-sm text-slate-500 mb-5 leading-relaxed">
                    {getScoreStatus(overallScore).text}
                  </p>

                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    {/* Metric 1 */}
                    <div className="bg-white rounded-2xl p-4 border border-slate-200/80 shadow-sm">
                      <div className="flex items-center justify-between text-xs font-semibold text-slate-500 mb-1">
                        <span>Hard Skills</span>
                        <span className="text-blue-600 font-bold">Coverage</span>
                      </div>
                      <div className="text-2xl font-black text-blue-600">
                        {matchData.skill_coverage_score.toFixed(1)}%
                      </div>
                      <p className="text-[11px] text-slate-400 mt-1">
                        <b>{matchData.matched_skills.length}</b> of <b>{matchData.total_jd_skills}</b> required skills
                      </p>
                    </div>

                    {/* Metric 2 */}
                    <div className="bg-white rounded-2xl p-4 border border-slate-200/80 shadow-sm">
                      <div className="flex items-center justify-between text-xs font-semibold text-slate-500 mb-1">
                        <span>Contextual Overlap</span>
                        <span className="text-purple-600 font-bold">TF-IDF</span>
                      </div>
                      <div className="text-2xl font-black text-purple-600">
                        {matchData.text_similarity_score.toFixed(1)}%
                      </div>
                      <p className="text-[11px] text-slate-400 mt-1">
                        Cosine n-gram textual alignment
                      </p>
                    </div>

                    {/* Metric 3 */}
                    <div className="bg-white rounded-2xl p-4 border border-slate-200/80 shadow-sm">
                      <div className="flex items-center justify-between text-xs font-semibold text-slate-500 mb-1">
                        <span>Missing Gaps</span>
                        <span className="text-rose-600 font-bold">Focus</span>
                      </div>
                      <div className="text-2xl font-black text-rose-600">
                        {matchData.missing_skills.length}
                      </div>
                      <p className="text-[11px] text-slate-400 mt-1">
                        Competencies to prioritize
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Action Bar / Download Toolbar */}
            <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm flex flex-wrap items-center justify-between gap-4">
              <div className="text-xs font-semibold text-slate-600 flex items-center space-x-2">
                <FileCheck className="w-4 h-4 text-emerald-600" />
                <span>Analysis ready for candidate export</span>
              </div>
              <div className="flex items-center space-x-3">
                <button
                  onClick={handleDownloadCsv}
                  className="px-4 py-2.5 rounded-xl text-xs font-bold bg-slate-900 hover:bg-slate-800 text-white flex items-center space-x-2 transition-all shadow-sm active:scale-95"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Download CSV Report</span>
                </button>
                <button
                  onClick={handleDownloadMarkdown}
                  className="px-4 py-2.5 rounded-xl text-xs font-bold bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200 flex items-center space-x-2 transition-all active:scale-95"
                >
                  <FileText className="w-3.5 h-3.5" />
                  <span>Executive Summary (.md)</span>
                </button>
              </div>
            </div>

            {/* Detailed Tabs Container */}
            <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">
              {/* Tab Navigation */}
              <div className="border-b border-slate-200 px-6 flex space-x-8 bg-slate-50/50">
                <button
                  onClick={() => setActiveTab('skills')}
                  className={`py-4 text-xs sm:text-sm font-bold border-b-2 transition-all flex items-center space-x-2 ${
                    activeTab === 'skills'
                      ? 'border-indigo-600 text-indigo-700'
                      : 'border-transparent text-slate-500 hover:text-slate-800'
                  }`}
                >
                  <Layers className="w-4 h-4" />
                  <span>Skill Pills</span>
                  <span className="text-[11px] bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full font-extrabold">
                    {matchData.matched_skills.length + matchData.missing_skills.length}
                  </span>
                </button>

                <button
                  onClick={() => setActiveTab('recs')}
                  className={`py-4 text-xs sm:text-sm font-bold border-b-2 transition-all flex items-center space-x-2 ${
                    activeTab === 'recs'
                      ? 'border-indigo-600 text-indigo-700'
                      : 'border-transparent text-slate-500 hover:text-slate-800'
                  }`}
                >
                  <BookOpen className="w-4 h-4" />
                  <span>Learning Pathways</span>
                  <span className="text-[11px] bg-rose-100 text-rose-700 px-2 py-0.5 rounded-full font-extrabold">
                    {results.recommendations.length}
                  </span>
                </button>

                <button
                  onClick={() => setActiveTab('table')}
                  className={`py-4 text-xs sm:text-sm font-bold border-b-2 transition-all flex items-center space-x-2 ${
                    activeTab === 'table'
                      ? 'border-indigo-600 text-indigo-700'
                      : 'border-transparent text-slate-500 hover:text-slate-800'
                  }`}
                >
                  <BarChart3 className="w-4 h-4" />
                  <span>Comparison Table</span>
                </button>

                <button
                  onClick={() => setActiveTab('domain')}
                  className={`py-4 text-xs sm:text-sm font-bold border-b-2 transition-all flex items-center space-x-2 ${
                    activeTab === 'domain'
                      ? 'border-indigo-600 text-indigo-700'
                      : 'border-transparent text-slate-500 hover:text-slate-800'
                  }`}
                >
                  <Briefcase className="w-4 h-4" />
                  <span>Domain Analytics</span>
                </button>
              </div>

              {/* Tab Contents */}
              <div className="p-6 sm:p-8">
                {/* TAB 1: Skills Breakdown */}
                {activeTab === 'skills' && (
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Matched Skills */}
                    <div className="rounded-2xl border border-emerald-200/80 bg-gradient-to-b from-emerald-50/40 to-white p-5 shadow-sm">
                      <div className="flex items-center space-x-2 mb-3">
                        <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                        <h4 className="font-bold text-emerald-950 text-sm">
                          Matched Skills ({matchData.matched_skills.length})
                        </h4>
                      </div>
                      <p className="text-xs text-slate-500 mb-4 leading-relaxed">
                        Skills detected in both the resume and the job posting:
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {matchData.matched_skills.map((skill) => (
                          <span
                            key={skill}
                            className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-xs font-bold bg-emerald-100/80 text-emerald-800 border border-emerald-300 shadow-sm"
                          >
                            <Check className="w-3.5 h-3.5 stroke-[2.5]" />
                            <span>{skill}</span>
                          </span>
                        ))}
                        {matchData.matched_skills.length === 0 && (
                          <span className="text-xs text-slate-400 italic">No matching skills detected.</span>
                        )}
                      </div>
                    </div>

                    {/* Missing Skills */}
                    <div className="rounded-2xl border border-rose-200/80 bg-gradient-to-b from-rose-50/40 to-white p-5 shadow-sm">
                      <div className="flex items-center space-x-2 mb-3">
                        <XCircle className="w-5 h-5 text-rose-600" />
                        <h4 className="font-bold text-rose-950 text-sm">
                          Skill Gaps ({matchData.missing_skills.length})
                        </h4>
                      </div>
                      <p className="text-xs text-slate-500 mb-4 leading-relaxed">
                        Required competencies not found in the resume:
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {matchData.missing_skills.map((skill) => (
                          <span
                            key={skill}
                            className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-xs font-bold bg-rose-100/80 text-rose-800 border border-rose-300 shadow-sm"
                          >
                            <span>✗ {skill}</span>
                          </span>
                        ))}
                        {matchData.missing_skills.length === 0 && (
                          <span className="text-xs text-emerald-700 font-bold">
                            🎉 100% hard skill match!
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Additional Skills */}
                    <div className="rounded-2xl border border-blue-200/80 bg-gradient-to-b from-blue-50/40 to-white p-5 shadow-sm">
                      <div className="flex items-center space-x-2 mb-3">
                        <Sparkles className="w-5 h-5 text-blue-600" />
                        <h4 className="font-bold text-blue-950 text-sm">
                          Candidate Strengths ({matchData.extra_skills.length})
                        </h4>
                      </div>
                      <p className="text-xs text-slate-500 mb-4 leading-relaxed">
                        Bonus strengths present in the resume beyond stated requirements:
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {matchData.extra_skills.map((skill) => (
                          <span
                            key={skill}
                            className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-xs font-bold bg-blue-100/80 text-blue-800 border border-blue-300 shadow-sm"
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
                    <div className="flex justify-between items-center mb-3">
                      <div>
                        <h4 className="text-sm font-bold text-slate-900">
                          Curated Learning Pathways & Upskilling Roadmaps
                        </h4>
                        <p className="text-xs text-slate-500">Official documentation, interactive courses, and project-based assignments</p>
                      </div>
                    </div>

                    {results.recommendations.length === 0 ? (
                      <div className="p-8 text-center text-emerald-700 font-bold bg-emerald-50 rounded-2xl border border-emerald-200">
                        🎉 Zero skill gaps detected! Your profile completely covers the hard skills for this posting.
                      </div>
                    ) : (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {results.recommendations.map((rec) => (
                          <div
                            key={rec.skill}
                            className="bg-white rounded-2xl border border-slate-200 p-5 hover:border-indigo-400 hover:shadow-md transition-all flex flex-col justify-between"
                          >
                            <div>
                              <div className="flex justify-between items-start mb-2.5">
                                <span className="font-extrabold text-slate-900 text-sm flex items-center space-x-2">
                                  <span>🎯 {rec.skill}</span>
                                </span>
                                <span className="text-[11px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 border border-slate-200">
                                  {rec.category}
                                </span>
                              </div>

                              <a
                                href={rec.url}
                                target="_blank"
                                rel="noreferrer"
                                className="text-indigo-600 hover:text-indigo-800 font-bold text-xs flex items-center space-x-1.5 mb-2.5 group"
                              >
                                <span className="group-hover:underline">{rec.title}</span>
                                <ExternalLink className="w-3.5 h-3.5 flex-shrink-0" />
                              </a>

                              <div className="flex items-center space-x-4 text-xs text-slate-500 mb-3">
                                <span>🏢 <b>{rec.platform}</b></span>
                                <span className="flex items-center space-x-1">
                                  <Clock className="w-3 h-3 text-slate-400" />
                                  <span>Est: <b>{rec.estimated_time}</b></span>
                                </span>
                              </div>

                              <div className="bg-slate-50 rounded-xl p-3 text-xs text-slate-700 border border-slate-100 leading-relaxed">
                                <b className="text-slate-900 font-bold">Suggested Project Action: </b>
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
                    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-4">
                      <div className="relative w-full sm:w-72">
                        <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
                        <input
                          type="text"
                          value={tableSearch}
                          onChange={(e) => setTableSearch(e.target.value)}
                          placeholder="Search skills, priority, or status..."
                          className="w-full pl-9 pr-3 py-2 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        />
                      </div>
                      <span className="text-xs text-slate-500 font-medium">
                        Showing {results.table_records.filter(r => r.Skill.toLowerCase().includes(tableSearch.toLowerCase())).length} skills
                      </span>
                    </div>

                    <div className="overflow-x-auto border border-slate-200 rounded-2xl shadow-sm">
                      <table className="w-full text-left text-xs">
                        <thead className="bg-slate-100/80 border-b border-slate-200 font-bold text-slate-600 uppercase tracking-wider text-[11px]">
                          <tr>
                            <th className="py-3.5 px-4">Skill</th>
                            <th className="py-3.5 px-4">Status</th>
                            <th className="py-3.5 px-4">Category</th>
                            <th className="py-3.5 px-4">Action Plan</th>
                            <th className="py-3.5 px-4">Resource</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-200 text-slate-700">
                          {results.table_records
                            .filter(r => r.Skill.toLowerCase().includes(tableSearch.toLowerCase()) || r.Status.toLowerCase().includes(tableSearch.toLowerCase()))
                            .map((row, idx) => (
                              <tr key={idx} className="hover:bg-indigo-50/30 transition-colors">
                                <td className="py-3.5 px-4 font-bold text-slate-900">{row.Skill}</td>
                                <td className="py-3.5 px-4">
                                  <span
                                    className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold ${
                                      row.Status.startsWith('Matched')
                                        ? 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                                        : row.Status.startsWith('Missing')
                                        ? 'bg-rose-100 text-rose-800 border border-rose-200'
                                        : 'bg-blue-100 text-blue-800 border border-blue-200'
                                    }`}
                                  >
                                    {row.Status.split('(')[0]}
                                  </span>
                                </td>
                                <td className="py-3.5 px-4 text-slate-500 font-medium">{row.Category}</td>
                                <td className="py-3.5 px-4 max-w-xs truncate text-slate-600">{row['Action / Recommendation']}</td>
                                <td className="py-3.5 px-4">
                                  {row['Learning Resource'] && row['Learning Resource'] !== 'N/A' ? (
                                    <a
                                      href={row['Learning Resource']}
                                      target="_blank"
                                      rel="noreferrer"
                                      className="text-indigo-600 hover:text-indigo-800 font-bold flex items-center space-x-1"
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
                    <h4 className="text-sm font-bold text-slate-900 mb-2">
                      Domain Alignment Breakdown
                    </h4>
                    <p className="text-xs text-slate-500 mb-6">
                      Visual comparison of skill alignment separated by engineering domain:
                    </p>

                    <div className="space-y-4 max-w-3xl">
                      {Object.entries(matchData.category_breakdown || {}).map(([cat, val]) => {
                        if (val.jd_required === 0 && val.matched === 0) return null;
                        const pct = val.jd_required > 0 ? Math.round((val.matched / val.jd_required) * 100) : 100;
                        return (
                          <div key={cat} className="bg-slate-50 rounded-2xl p-4 border border-slate-200">
                            <div className="flex justify-between text-xs font-bold text-slate-800 mb-1.5">
                              <span>{cat}</span>
                              <span className="text-indigo-700">{val.matched} / {val.jd_required} matched ({pct}%)</span>
                            </div>
                            <div className="w-full bg-slate-200 rounded-full h-2.5 overflow-hidden">
                              <div
                                className="bg-gradient-to-r from-blue-600 to-indigo-600 h-full rounded-full transition-all duration-700"
                                style={{ width: `${pct}%` }}
                              />
                            </div>
                            <div className="flex space-x-4 text-[11px] text-slate-500 mt-2 font-medium">
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
      {/* <footer className="bg-white border-t border-slate-200/80 py-6 text-center text-xs text-slate-500">
        <p className="font-medium">
          CareerMatch AI • Resume Analyzer & Job Fit Predictor • Built with Python, PyMuPDF, Scikit-learn, React 18 & Tailwind CSS
        </p>
      </footer> */}
      



<footer className="relative overflow-hidden border-t border-slate-200 bg-gradient-to-b from-white to-slate-50 px-6 py-8">
  <div className="mx-auto max-w-7xl">

    <div className="flex flex-col items-center justify-between gap-6 md:flex-row">

      {/* Brand */}
      <div className="text-center md:text-left">
        <h3 className="text-xl font-extrabold tracking-tight text-slate-900">
          CareerMatch <span className="bg-gradient-to-r from-blue-600 to-violet-600 bg-clip-text text-transparent">AI</span>
        </h3>

        <p className="mt-1 text-sm text-slate-500">
          Smart Resume Analysis. Better Career Decisions.
        </p>
      </div>

      {/* Technology Stack */}
      <div className="flex flex-wrap justify-center gap-2">
        {["Python", "React 18", "Tailwind CSS", "Scikit-learn", "PyMuPDF"].map((tech) => (
<span
  key={tech}
  className="cursor-pointer rounded-full border border-slate-200 bg-white px-4 py-2 text-xs font-semibold text-slate-600 shadow-sm
  transition-all duration-300 ease-out
  hover:-translate-y-1
  hover:scale-110
  hover:border-blue-500
  hover:bg-blue-600
  hover:text-white
  hover:shadow-lg
  hover:shadow-blue-200/60"
>
  {tech}
</span>
        ))}
      </div>
    </div>

    {/* Bottom Section */}
    <div className="mt-7 flex flex-col items-center justify-between gap-3 border-t border-slate-200 pt-5 text-center sm:flex-row">

      <p className="text-xs text-slate-500">
        © {new Date().getFullYear()} CareerMatch AI. All rights reserved.
      </p>

      <p className="flex items-center gap-1.5 text-xs text-slate-500">
        Crafted with
        <span className="text-red-500">♥</span>
        for smarter career growth.
      </p>

    </div>
  </div>
</footer>
      
    </div>
  );
}
