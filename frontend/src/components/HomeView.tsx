import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { BookOpen, Calendar, CheckCircle, Clock, ArrowRight } from 'lucide-react';
import { UserProfile } from '../types';

interface PlannerItem {
  plannable: {
    title: string;
    due_at?: string;
    points_possible?: number;
  };
  context_name: string;
  plannable_type: string;
  html_url?: string;
}

interface DashboardCard {
  id: number;
  longName: string;
  shortName: string;
  courseCode?: string;
  term?: string;
  image?: string;
}

interface HomeViewProps {
  token: string;
  user: UserProfile | null;
  onSelectCourse: (course: any) => void;
}

export const HomeView: React.FC<HomeViewProps> = ({ token, user, onSelectCourse }) => {
  const [plannerItems, setPlannerItems] = useState<PlannerItem[]>([]);
  const [dashboardCards, setDashboardCards] = useState<DashboardCard[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const response = await fetch('http://localhost:8001/api/dashboard', {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        if (response.ok) {
          const data = await response.json();
          setPlannerItems(data.planner_items || []);
          setDashboardCards(data.dashboard_cards || []);
        }
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [token]);

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'No due date';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-gray-400">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <div className="p-8 h-full overflow-y-auto">
      {/* Welcome Section */}
      <div className="mb-10">
        <h1 className="text-3xl font-serif font-bold text-gray-900 mb-2">
          Welcome back, {user?.short_name || user?.name || 'Scholar'}
        </h1>
        <p className="text-gray-500">
          You have {plannerItems.length} upcoming tasks this week.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Column: Active Courses */}
        <div className="lg:col-span-2 space-y-8">
          <section>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
                <BookOpen size={20} className="text-terracotta" />
                Active Courses
              </h2>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {dashboardCards.length > 0 ? (
                dashboardCards.map((card) => (
                  <motion.div
                    key={card.id}
                    whileHover={{ y: -2 }}
                    className="bg-white p-5 rounded-xl shadow-sm border border-gray-200 cursor-pointer hover:shadow-md transition-all"
                    onClick={() => onSelectCourse({ id: card.id, name: card.longName, course_code: card.shortName })}
                  >
                    <div className="flex justify-between items-start mb-3">
                      <div className="w-10 h-10 rounded-lg bg-orange-50 flex items-center justify-center text-terracotta">
                        <BookOpen size={20} />
                      </div>
                      {card.term && (
                        <span className="text-xs font-medium px-2 py-1 bg-gray-100 rounded-full text-gray-500">
                          {card.term}
                        </span>
                      )}
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-1 line-clamp-1" title={card.longName}>
                      {card.longName}
                    </h3>
                    <p className="text-sm text-gray-500 mb-4">{card.shortName}</p>
                    <div className="flex items-center text-sm text-terracotta font-medium">
                      View Course <ArrowRight size={14} className="ml-1" />
                    </div>
                  </motion.div>
                ))
              ) : (
                <div className="col-span-2 bg-gray-50 rounded-xl p-8 text-center text-gray-500">
                  No active courses found.
                </div>
              )}
            </div>
          </section>
        </div>

        {/* Side Column: Upcoming Tasks */}
        <div className="space-y-8">
          <section>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
                <Calendar size={20} className="text-terracotta" />
                Upcoming Tasks
              </h2>
            </div>
            
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
              {plannerItems.length > 0 ? (
                <div className="divide-y divide-gray-100">
                  {plannerItems.slice(0, 5).map((item, index) => (
                    <div key={index} className="p-4 hover:bg-gray-50 transition-colors">
                      <div className="flex items-start gap-3">
                        <div className={`mt-1 w-5 h-5 rounded-full border-2 flex items-center justify-center flex-shrink-0 ${
                          item.plannable_type === 'grading' ? 'border-purple-200 text-purple-600' : 'border-orange-200 text-orange-600'
                        }`}>
                          {item.plannable_type === 'grading' ? <CheckCircle size={12} /> : <Clock size={12} />}
                        </div>
                        <div>
                          <h4 className="text-sm font-medium text-gray-900 line-clamp-1">
                            {item.plannable.title}
                          </h4>
                          <p className="text-xs text-gray-500 mt-0.5">
                            {item.context_name}
                          </p>
                          <div className="flex items-center gap-2 mt-2">
                            <span className="text-xs font-medium text-gray-400 bg-gray-100 px-1.5 py-0.5 rounded">
                              {formatDate(item.plannable.due_at)}
                            </span>
                            {item.plannable.points_possible && (
                              <span className="text-xs text-gray-400">
                                {item.plannable.points_possible} pts
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="p-8 text-center text-gray-500 text-sm">
                  No upcoming tasks.
                </div>
              )}
              
              <div className="p-3 bg-gray-50 border-t border-gray-100 text-center">
                <button className="text-sm font-medium text-terracotta hover:text-terracotta-dark">
                  View All Tasks
                </button>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
};
