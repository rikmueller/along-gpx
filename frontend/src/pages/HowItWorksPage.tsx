import { Link } from 'react-router-dom'
import MarketingLayout from '../components/MarketingLayout'
import SeoMeta from '../components/SeoMeta'
import './MarketingPages.css'

export default function HowItWorksPage() {
  return (
    <MarketingLayout>
      <SeoMeta
        title="How it works | WhatsAround"
        description="See how WhatsAround turns routes into structured insights with filters, live mapping, and export-ready outputs."
        url="https://getwhatsaround.app/how-it-works"
      />

      <section className="marketing-container marketing-hero">
        <h1>How it works.</h1>

        <div className="marketing-hero-actions">
          {/* Placeholder for layout consistency */}
        </div>
      </section>

      <section className="marketing-container">
        <div className="marketing-steps">
          <div className="marketing-step">
            <span>Step 1</span>
            <h4>Choose your input</h4>
            <p>Upload a GPX route or place a map marker to define where you want to search.</p>
          </div>
          <div className="marketing-step">
            <span>Step 2</span>
            <h4>Select filters</h4>
            <p>Use presets or add custom include/exclude tags to focus on the POIs that matter to you.</p>
          </div>
          <div className="marketing-step">
            <span>Step 3</span>
            <h4>Run the search</h4>
            <p>WhatsAround batches Overpass API queries and streams results as they appear in the App.</p>
          </div>
          <div className="marketing-step">
            <span>Step 4</span>
            <h4>Export & share</h4>
            <p>Download Excel summaries or interactive HTML maps to share with teams or keep for reference.</p>
          </div>
        </div>

        <div className="marketing-cta-panel">
          <div>
            <h3>Ready to try it?</h3>
            <p>Launch the App and start discovering nearby insights in minutes.</p>
          </div>
          <Link to="/app" className="marketing-button primary">
            Open App
          </Link>
        </div>
      </section>
    </MarketingLayout>
  )
}
