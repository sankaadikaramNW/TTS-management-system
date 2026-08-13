import React from 'react'

export const CourseCalendarPrintView = ({ course, entries, onClose }) => {
  // Format date helper: YYYY-MM-DD -> DD.MM.YYYY
  const formatDateDisplay = (dateStr) => {
    if (!dateStr) return '-'
    const parts = dateStr.split('-')
    if (parts.length === 3) {
      return `${parts[2]}.${parts[1]}.${parts[0]}`
    }
    return dateStr
  }

  // Calculated totals
  const totalTheory = entries.reduce((acc, curr) => acc + (Number(curr.theory_periods) || 0), 0)
  const totalPractical = entries.reduce((acc, curr) => acc + (Number(curr.practical_periods) || 0), 0)
  const totalPeriods = entries.reduce((acc, curr) => acc + (Number(curr.total_periods) || 0), 0)
  const totalWorkingDays = entries.reduce((acc, curr) => acc + (Number(curr.working_days) || 0), 0)

  const handleTriggerPrint = () => {
    window.print()
  }

  return (
    <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.6)', zIndex: 1060 }} tabIndex="-1">
      <div className="modal-dialog modal-xl modal-dialog-scrollable">
        <div className="modal-content shadow-lg border-0">
          <div className="modal-header bg-dark text-white p-3 no-print">
            <h5 className="modal-title fw-bold">
              <i className="bi bi-printer me-2"></i> Official Course Calendar — Print Preview
            </h5>
            <div className="d-flex gap-2">
              <button className="btn btn-sm btn-success fw-semibold" onClick={handleTriggerPrint}>
                <i className="bi bi-printer-fill me-1"></i> Print / Save as PDF
              </button>
              <button className="btn btn-sm btn-outline-light" onClick={onClose}>
                <i className="bi bi-x-lg"></i> Close
              </button>
            </div>
          </div>

          <div className="modal-body p-4 p-md-5 bg-white text-dark printable-document" id="printable-calendar-area">
            {/* SLAF TTS Official Header */}
            <div className="text-center mb-4 border-bottom pb-3">
              <div className="d-flex justify-content-center align-items-center mb-2">
                <i className="bi bi-shield-shaded text-primary me-2 fs-2"></i>
                <h3 className="fw-extrabold text-uppercase display-font mb-0" style={{ letterSpacing: '1px' }}>
                  SRI LANKA AIR FORCE
                </h3>
              </div>
              <h5 className="fw-bold text-uppercase text-secondary mb-1">
                TRADE TRAINING SCHOOL — EKALA
              </h5>
              <h6 className="fw-extrabold text-uppercase text-primary tracking-wide mb-0">
                COURSE CALENDAR / SYLLABUS SCHEDULE
              </h6>
            </div>

            {/* Course Metadata Card */}
            {course && (
              <div className="border rounded p-3 mb-4 bg-light shadow-xs">
                <div className="row g-2 text-dark">
                  <div className="col-md-7">
                    <span className="text-muted small fw-bold text-uppercase d-block">Course Title</span>
                    <h5 className="fw-extrabold mb-0 text-primary">{course.name}</h5>
                    <small className="text-muted fw-semibold">Code: {course.code} | Trade: {course.trade_name || course.trade?.label || 'General'}</small>
                  </div>
                  <div className="col-md-5 border-start-md ps-md-3">
                    <div className="row g-2 small">
                      <div className="col-6">
                        <span className="text-muted d-block">Intake / Batch:</span>
                        <strong className="text-dark">{course.batches?.[0]?.name || 'Current Intake'}</strong>
                      </div>
                      <div className="col-6">
                        <span className="text-muted d-block">Duration:</span>
                        <strong className="text-dark">{course.duration_weeks || 24} Weeks</strong>
                      </div>
                      <div className="col-6">
                        <span className="text-muted d-block">Start Date:</span>
                        <strong className="text-dark">{formatDateDisplay(course.start_date)}</strong>
                      </div>
                      <div className="col-6">
                        <span className="text-muted d-block">End Date:</span>
                        <strong className="text-dark">{formatDateDisplay(course.end_date)}</strong>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Main Course Calendar Table */}
            <div className="table-responsive mb-4">
              <table className="table table-bordered align-middle text-center border-secondary mb-0" style={{ fontSize: '0.85rem' }}>
                <thead className="table-dark text-uppercase small align-middle">
                  <tr>
                    <th style={{ width: '45px' }}>S/No</th>
                    <th className="text-start" style={{ minWidth: '220px' }}>Phase / Activity</th>
                    <th style={{ width: '90px' }}>No. of Theory Periods</th>
                    <th style={{ width: '90px' }}>No. of Practical Periods</th>
                    <th style={{ width: '85px' }}>Total Periods</th>
                    <th style={{ width: '85px' }}>No. of Working Days</th>
                    <th style={{ width: '105px' }}>Dates of Commencement</th>
                    <th style={{ width: '105px' }}>Dates of Completion</th>
                    <th className="text-start" style={{ minWidth: '150px' }}>Instructor</th>
                    <th className="text-start" style={{ minWidth: '160px' }}>Remarks</th>
                  </tr>
                </thead>
                <tbody>
                  {entries && entries.length > 0 ? (
                    entries.map((item, idx) => (
                      <tr key={item.id || idx}>
                        <td className="fw-bold">{String(item.serial_number || idx + 1).padStart(2, '0')}</td>
                        <td className="text-start fw-semibold">{item.phase_name}</td>
                        <td>{item.theory_periods > 0 ? item.theory_periods : '-'}</td>
                        <td>{item.practical_periods > 0 ? item.practical_periods : '-'}</td>
                        <td className="fw-bold bg-light">{item.total_periods > 0 ? item.total_periods : '-'}</td>
                        <td>{item.working_days > 0 ? item.working_days : '-'}</td>
                        <td className="fw-semibold">{formatDateDisplay(item.commencement_date)}</td>
                        <td className="fw-semibold">{formatDateDisplay(item.completion_date)}</td>
                        <td className="text-start small">
                          {item.instructor_status === 'ASSIGNED' && item.instructor_name ? (
                            <span className="fw-semibold text-dark">{item.instructor_name}</span>
                          ) : (
                            <span className="fw-bold text-danger">INSTRUCTOR NOT ASSIGNED</span>
                          )}
                        </td>
                        <td className="text-start small">
                          {item.remarks ? item.remarks : '-'}
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="10" className="py-4 text-muted">
                        No phase entries defined for this course calendar.
                      </td>
                    </tr>
                  )}
                </tbody>
                {entries && entries.length > 0 && (
                  <tfoot className="table-light fw-bold align-middle">
                    <tr className="border-top border-2 border-dark">
                      <td colSpan="2" className="text-end text-uppercase pe-3">Grand Totals:</td>
                      <td className="text-primary">{totalTheory}</td>
                      <td className="text-primary">{totalPractical}</td>
                      <td className="bg-primary text-white">{totalPeriods}</td>
                      <td className="text-dark">{totalWorkingDays}</td>
                      <td colSpan="4" className="text-start small text-muted ps-3">
                        Total Course Phases: {entries.length}
                      </td>
                    </tr>
                  </tfoot>
                )}
              </table>
            </div>

            {/* Official Signature Blocks */}
            <div className="row mt-5 pt-4 text-center signature-section" style={{ fontSize: '0.825rem' }}>
              <div className="col-4">
                <div className="border-top border-dark pt-2 mx-3">
                  <p className="fw-bold mb-0">Prepared By</p>
                  <p className="text-muted small mb-0">Course Coordinator / Instructor</p>
                  <p className="text-muted extra-small">Date: ........................</p>
                </div>
              </div>
              <div className="col-4">
                <div className="border-top border-dark pt-2 mx-3">
                  <p className="fw-bold mb-0">Checked By</p>
                  <p className="text-muted small mb-0">Chief Instructor (CI) - TTS</p>
                  <p className="text-muted extra-small">Date: ........................</p>
                </div>
              </div>
              <div className="col-4">
                <div className="border-top border-dark pt-2 mx-3">
                  <p className="fw-bold mb-0">Approved By</p>
                  <p className="text-muted small mb-0">Officer Commanding Training (OCT)</p>
                  <p className="text-muted extra-small">Date: ........................</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Embedded CSS for clean A4 printing */}
      <style>{`
        @media print {
          body * {
            visibility: hidden;
          }
          #printable-calendar-area, #printable-calendar-area * {
            visibility: visible;
          }
          #printable-calendar-area {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            padding: 20px !important;
          }
          .no-print {
            display: none !important;
          }
          .modal {
            position: static !important;
            background: none !important;
          }
          .modal-dialog {
            max-width: 100% !important;
            margin: 0 !important;
          }
          .modal-content {
            border: none !important;
            box-shadow: none !important;
          }
        }
      `}</style>
    </div>
  )
}

export default CourseCalendarPrintView
