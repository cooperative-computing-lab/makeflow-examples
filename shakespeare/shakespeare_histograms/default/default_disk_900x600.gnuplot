load "default_disk_vars.gnuplot"
set terminal pngcairo truecolor rounded size 900,600 enhanced font "times,12"
set output "default_disk_900x600.png"
unset key
unset border
set style line 1 lc 16
set style fill solid noborder
set tmargin 2
set bmargin 2
unset tics
set arrow from current_minimum,graph -0.01 to current_percentile25,graph -0.01 nohead lc 16
set arrow from current_percentile75,graph -0.01 to current_maximum,graph -0.01 nohead lc 16
set label "" at current_mean,graph -0.00 tc ls 1 center front point pt 4
set label sprintf("%.0f", current_mode) at current_mode,graph -0.05 tc ls 1 center front point pt 8 offset 0,character -0.90
set label "" at current_first_allocation,graph -0.025 tc ls 1 center front point pt 10
set label sprintf("%.0f", all_minimum) at all_minimum,graph -0.01 tc ls 1 right front nopoint offset character -1.0,character -0.25
set label sprintf("%.0f", all_maximum) at all_maximum,graph -0.01 tc ls 1 left  front nopoint offset character  1.0,character -0.25
set boxwidth (all_maximum - all_minimum + 1)/50 absolute
set xrange [all_minimum - 1 : all_maximum + 2]
set yrange [0:(log10(all_mode_count))]
set label sprintf("log(%d)",current_mode_count) at current_mode,(log10(current_mode_count)) tc ls 1 left front nopoint offset 0,character 0.5
plot "default_disk_table.data" using 1:(log10($2)) w boxes

