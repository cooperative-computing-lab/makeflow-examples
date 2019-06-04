load "default_cores_avg_vars.gnuplot"
set terminal pngcairo truecolor rounded size 372,248 enhanced font "times,10"
set output "default_cores_avg_372x248.png"
unset key
unset border
set style line 1 lc 16
set style fill solid noborder
set tmargin 2
set bmargin 2
unset tics
set arrow from current_minimum,graph -0.01 to current_percentile25,graph -0.01 nohead lc 16
set arrow from current_percentile75,graph -0.01 to current_maximum,graph -0.01 nohead lc 16
set label "" at current_mean,graph 0.00 tc ls 1 center front point pt 4
set label sprintf("%.0f", current_mode) at current_mode,graph -0.05 tc ls 1 center front point pt 8 offset 0,character -0.90
set label "" at current_first_allocation,graph -0.025 tc ls 1 center front point pt 10
set label sprintf("%.0f", current_minimum) at current_minimum,graph -0.01 tc ls 1 right front nopoint offset character -1.0,character -0.25
set label sprintf("%.0f", current_maximum) at current_maximum,graph -0.01 tc ls 1 left front nopoint offset character 1.0,character -0.25
gap = (all_maximum - all_minimum)/5.0
set boxwidth (0.1 > current_bin_size ? 0.1 : current_bin_size) absolute
set xrange [all_minimum - gap : all_maximum + gap]
set yrange [0:(log10(all_mode_count))]
set label sprintf("log(%d)",current_mode_count) at current_mode,(log10(current_mode_count)) tc ls 1 left front nopoint offset 0,character 0.5
plot "default_cores_avg_table.data" using 1:(log10($2)) w boxes

