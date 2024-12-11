import React, { ReactNode } from 'react';

// Define types for table props and column definition
export interface TableColumn<T> {
  key: string;
  header: string;
  render?: (item: T) => ReactNode;
  sortable?: boolean;
  className?: string;
}

export interface TableProps<T> {
  columns: TableColumn<T>[];
  data: T[];
  title?: string;
  onRowClick?: (item: T) => void;
  className?: string;
  emptyState?: ReactNode;
  loading?: boolean;
}

export function Table<T>({
  columns, 
  data, 
  title, 
  onRowClick, 
  className = '',
  emptyState,
  loading
}: TableProps<T>) {
  return (
    <div className={`bg-white rounded-lg shadow-md overflow-hidden ${className}`}>
      {title && (
        <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
          <h3 className="text-xl font-semibold text-gray-800">{title}</h3>
        </div>
      )}
      
      {loading ? (
        <div className="flex justify-center items-center h-48">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      ) : data.length === 0 ? (
        emptyState || (
          <div className="text-center py-12 text-gray-500">
            No data available
          </div>
        )
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-100 border-b border-gray-200">
              <tr>
                {columns.map((column) => (
                  <th 
                    key={column.key}
                    className={`
                      px-6 py-3 
                      text-left text-xs 
                      font-medium text-gray-600 
                      uppercase tracking-wider
                      ${column.className || ''}
                    `}
                  >
                    {column.header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {data.map((item, rowIndex) => (
                <tr 
                  key={rowIndex}
                  className={`
                    hover:bg-gray-50 
                    transition-colors 
                    duration-200
                    ${onRowClick ? 'cursor-pointer' : ''}
                  `}
                  onClick={() => onRowClick && onRowClick(item)}
                >
                  {columns.map((column) => (
                    <td 
                      key={column.key}
                      className={`
                        px-6 py-4 
                        text-sm text-gray-900
                        ${column.className || ''}
                      `}
                    >
                      {column.render 
                        ? column.render(item) 
                        : (item as any)[column.key]
                      }
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

// Optional: Example Specialized Tables for PropMaster AI domains
export function PropTable() {
  // Specialized prop table implementation
}

export function InsightTable() {
  // Specialized insight table implementation
}

export function SentimentTable() {
  // Specialized sentiment table implementation
}