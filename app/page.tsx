export default function Home() {
  // Helper to generate random number between 1 and 9
  const rand = () => Math.floor(Math.random() * 9) + 1;

  return (
    <div className="flex flex-col gap-1 bg-white p-10">
      {Array.from({ length: 3 }).map((_, rowBlock) => (
        <div key={rowBlock} className="flex gap-1">
          {Array.from({ length: 3 }).map((_, colBlock) => (
            <div
              key={colBlock}
              className="bg-amber-600 flex flex-col gap-1 p-1"
            >
              {Array.from({ length: 3 }).map((_, row) => (
                <div key={row} className="flex gap-1">
                  {Array.from({ length: 3 }).map((_, col) => (
                    <div
                      key={col}
                      className="bg-blue-600 size-12 flex items-center justify-center text-white text-lg font-semibold"
                    >
                      {rand()}
                    </div>
                  ))}
                </div>
              ))}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}
