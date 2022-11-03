defmodule Detector do
  def better_than_average(class_points, your_points) do
    your_points > Enum.reduce(class_points, fn (score, sum) -> sum + score end) / length(class_points)
  end
end

defmodule Finder do
  def find_needle(haystack) do
    Enum.
  end
end
