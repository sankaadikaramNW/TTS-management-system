import React from 'react'
import { ClassicalReportModal } from '../../components/ClassicalReportModal'

export const CourseCalendarPrintView = ({ course, entries, onClose }) => {
  return (
    <ClassicalReportModal
      show={true}
      onClose={onClose}
      title={`COURSE TRAINING CALENDAR & SCHEDULE — ${course?.name || 'Course'} (${course?.code || 'CODE'})`}
      endpoint="/api/v1/reports/course-calendar"
      params={{ course_id: course?.id }}
      defaultOrientation="landscape"
    />
  )
}

export default CourseCalendarPrintView
