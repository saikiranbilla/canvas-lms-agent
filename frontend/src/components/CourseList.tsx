import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { BookOpen, Users, ArrowRight } from 'lucide-react';

interface Course {
  id: number;
  name: string;
  course_code: string;
  total_students?: number;
  term?: { name: string };
}

interface CourseListProps {
  token: string;
  onSelectCourse: (course: Course) => void;
}

export const CourseList: React.FC<CourseListProps> = ({ token, onSelectCourse }) => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await fetch('http://localhost:8001/api/courses', {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        setCourses(data.courses || []);
      } catch (error) {
        console.error('Failed to fetch courses:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCourses();
  }, [token]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-gray-500">Loading courses...</div>
      </div>
    );
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8 font-serif">My Courses</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {courses.map((course) => (
          <motion.div
            key={course.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="p-3 bg-orange-50 rounded-lg">
                <BookOpen className="text-orange-600" size={24} />
              </div>
              {course.term && (
                <span className="text-xs font-medium px-2 py-1 bg-gray-100 rounded-full text-gray-600">
                  {course.term.name}
                </span>
              )}
            </div>
            
            <h3 className="text-xl font-semibold mb-2 text-gray-900">{course.name}</h3>
            <p className="text-gray-500 text-sm mb-4">{course.course_code}</p>
            
            <div className="flex items-center gap-4 text-sm text-gray-500 mb-6">
              <div className="flex items-center gap-1">
                <Users size={16} />
                <span>{course.total_students || 0} Students</span>
              </div>
            </div>

            <button
              onClick={() => onSelectCourse(course)}
              className="w-full py-2 px-4 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition-colors flex items-center justify-center gap-2"
            >
              Manage Course <ArrowRight size={16} />
            </button>
          </motion.div>
        ))}
      </div>
    </div>
  );
};
