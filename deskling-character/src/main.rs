use eframe::egui;
use std::time::{Duration, Instant};

fn main() -> Result<(), eframe::Error> {
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_inner_size([300.0, 400.0])
            .with_transparent(true)
            .with_decorations(false)
            .with_always_on_top()
            .with_resizable(false),
        ..Default::default()
    };

    eframe::run_native(
        "Deskling Character",
        options,
        Box::new(|_cc| Ok(Box::new(DesklingApp::new()))),
    )
}

struct DesklingApp {
    messages: Vec<&'static str>,
    current_message_index: usize,
    speech_bubble_visible: bool,
    speech_bubble_timer: Option<Instant>,
    animation_time: f32,
    character_state: CharacterState,
}

#[derive(Debug, Clone, Copy, PartialEq)]
enum CharacterState {
    Idle,
    Talking,
}

impl Default for DesklingApp {
    fn default() -> Self {
        Self::new()
    }
}

impl DesklingApp {
    fn new() -> Self {
        Self {
            messages: vec![
                "Hi there! 👋",
                "I'm Deskling, your desktop buddy!",
                "Drag me anywhere you like!",
                "Click me again for another message!",
                "I can show text in speech bubbles!",
                "Having fun yet? 😊",
                "I'm a simple stickman for now!",
                "This is the MVP demo in Rust!",
                "More features coming soon!",
                "Built with egui and Rust!",
            ],
            current_message_index: 0,
            speech_bubble_visible: false,
            speech_bubble_timer: None,
            animation_time: 0.0,
            character_state: CharacterState::Idle,
        }
    }

    fn show_speech_bubble(&mut self, message: &str, ui: &mut egui::Ui, character_center: egui::Pos2) {
        let bubble_rect = egui::Rect::from_center_size(
            egui::pos2(character_center.x, 60.0),
            egui::vec2(250.0, 60.0),
        );

        // Draw speech bubble background
        ui.painter().rect_filled(
            bubble_rect,
            20.0,
            egui::Color32::from_rgba_unmultiplied(255, 255, 255, 242),
        );

        // Draw border
        ui.painter().rect_stroke(
            bubble_rect,
            20.0,
            egui::Stroke::new(2.0, egui::Color32::from_rgb(51, 51, 51)),
            egui::StrokeKind::Outside,
        );

        // Draw pointer triangle (pointing down to character)
        let triangle_points = [
            egui::pos2(character_center.x - 15.0, bubble_rect.max.y),
            egui::pos2(character_center.x + 15.0, bubble_rect.max.y),
            egui::pos2(character_center.x, bubble_rect.max.y + 15.0),
        ];
        ui.painter().add(egui::Shape::convex_polygon(
            triangle_points.to_vec(),
            egui::Color32::from_rgba_unmultiplied(255, 255, 255, 242),
            egui::Stroke::NONE,
        ));

        // Draw text
        ui.painter().text(
            bubble_rect.center(),
            egui::Align2::CENTER_CENTER,
            message,
            egui::FontId::proportional(14.0),
            egui::Color32::from_rgb(51, 51, 51),
        );
    }

    fn draw_stickman(&self, ui: &mut egui::Ui, center: egui::Pos2, scale: f32) {
        let painter = ui.painter();
        let color = egui::Color32::from_rgb(51, 51, 51);
        let stroke = egui::Stroke::new(4.0 * scale, color);
        let thin_stroke = egui::Stroke::new(2.0 * scale, egui::Color32::BLACK);

        // Apply bounce animation
        let bounce_offset = if self.character_state == CharacterState::Idle {
            (self.animation_time * 3.14).sin() * 10.0 * scale
        } else {
            (self.animation_time * 12.0).sin() * 5.0 * scale
        };

        let head_center = egui::pos2(center.x, center.y - 60.0 * scale + bounce_offset);

        // Head
        painter.circle_filled(head_center, 20.0 * scale, color);
        painter.circle_stroke(head_center, 20.0 * scale, thin_stroke);

        // Eyes
        let left_eye = egui::pos2(head_center.x - 8.0 * scale, head_center.y - 2.0 * scale);
        let right_eye = egui::pos2(head_center.x + 8.0 * scale, head_center.y - 2.0 * scale);
        painter.circle_filled(left_eye, 3.0 * scale, egui::Color32::WHITE);
        painter.circle_filled(right_eye, 3.0 * scale, egui::Color32::WHITE);
        painter.circle_filled(
            egui::pos2(left_eye.x + 1.0 * scale, left_eye.y),
            1.5 * scale,
            egui::Color32::BLACK,
        );
        painter.circle_filled(
            egui::pos2(right_eye.x + 1.0 * scale, right_eye.y),
            1.5 * scale,
            egui::Color32::BLACK,
        );

        // Smile (using a curved line approximation)
        let smile_y = head_center.y + 5.0 * scale;
        let smile_points: Vec<egui::Pos2> = (0..20)
            .map(|i| {
                let t = i as f32 / 19.0;
                let x = head_center.x + (t - 0.5) * 40.0 * scale;
                let curve = ((t - 0.5) * 3.14).sin() * 5.0 * scale;
                egui::pos2(x, smile_y + curve)
            })
            .collect();
        for i in 0..smile_points.len() - 1 {
            painter.line_segment([smile_points[i], smile_points[i + 1]], thin_stroke);
        }

        // Body
        let body_top = egui::pos2(center.x, center.y - 40.0 * scale + bounce_offset);
        let body_bottom = egui::pos2(center.x, center.y + 10.0 * scale + bounce_offset);
        painter.line_segment([body_top, body_bottom], stroke);

        // Arms
        let arm_y = center.y - 25.0 * scale + bounce_offset;
        painter.line_segment(
            [
                egui::pos2(center.x, arm_y),
                egui::pos2(center.x - 25.0 * scale, arm_y + 20.0 * scale),
            ],
            stroke,
        );
        painter.line_segment(
            [
                egui::pos2(center.x, arm_y),
                egui::pos2(center.x + 25.0 * scale, arm_y + 20.0 * scale),
            ],
            stroke,
        );

        // Legs
        painter.line_segment(
            [
                body_bottom,
                egui::pos2(center.x - 20.0 * scale, center.y + 50.0 * scale + bounce_offset),
            ],
            stroke,
        );
        painter.line_segment(
            [
                body_bottom,
                egui::pos2(center.x + 20.0 * scale, center.y + 50.0 * scale + bounce_offset),
            ],
            stroke,
        );

        // Feet
        let left_foot_y = center.y + 50.0 * scale + bounce_offset;
        let right_foot_y = center.y + 50.0 * scale + bounce_offset;
        painter.line_segment(
            [
                egui::pos2(center.x - 20.0 * scale, left_foot_y),
                egui::pos2(center.x - 30.0 * scale, left_foot_y),
            ],
            egui::Stroke::new(3.0 * scale, color),
        );
        painter.line_segment(
            [
                egui::pos2(center.x + 20.0 * scale, right_foot_y),
                egui::pos2(center.x + 30.0 * scale, right_foot_y),
            ],
            egui::Stroke::new(3.0 * scale, color),
        );
    }
}

impl eframe::App for DesklingApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        // Update animation time
        self.animation_time += ctx.input(|i| i.stable_dt);

        // Check if speech bubble should be hidden
        if let Some(timer) = self.speech_bubble_timer {
            if timer.elapsed() > Duration::from_secs(3) {
                self.speech_bubble_visible = false;
                self.speech_bubble_timer = None;
                self.character_state = CharacterState::Idle;
            }
        }

        // Request continuous repaint for animations
        ctx.request_repaint_after(Duration::from_millis(16)); // ~60 FPS

        egui::CentralPanel::default()
            .frame(egui::Frame::new().fill(egui::Color32::TRANSPARENT))
            .show(ctx, |ui| {
                // Make the window draggable
                let response = ui.allocate_rect(ui.available_rect_before_wrap(), egui::Sense::drag());
                
                if response.dragged() {
                    // Window dragging is handled automatically by egui for frameless windows
                }

                let character_center = egui::pos2(150.0, 250.0);
                let character_radius = 60.0;

                // Check for character click
                if let Some(mouse_pos) = ctx.input(|i| i.pointer.interact_pos()) {
                    if ctx.input(|i| i.pointer.primary_clicked()) {
                        let distance = mouse_pos.distance(character_center);
                        if distance < character_radius {
                            // Clicked on character - show next message
                            self.speech_bubble_visible = true;
                            self.speech_bubble_timer = Some(Instant::now());
                            self.character_state = CharacterState::Talking;
                            self.current_message_index =
                                (self.current_message_index + 1) % self.messages.len();
                        }
                    }
                }

                // Draw speech bubble if visible
                if self.speech_bubble_visible {
                    let message = self.messages[self.current_message_index];
                    self.show_speech_bubble(message, ui, character_center);
                }

                // Check hover state for scale
                let scale = if let Some(mouse_pos) = ctx.input(|i| i.pointer.hover_pos()) {
                    let distance = mouse_pos.distance(character_center);
                    if distance < character_radius {
                        1.1 // Zoom on hover
                    } else {
                        1.0
                    }
                } else {
                    1.0
                };

                // Draw the stickman character
                self.draw_stickman(ui, character_center, scale);

                // Status hint (fades after initial display)
                if self.animation_time < 3.0 {
                    let alpha = ((3.0 - self.animation_time) * 255.0 / 3.0) as u8;
                    ui.painter().text(
                        egui::pos2(150.0, 380.0),
                        egui::Align2::CENTER_CENTER,
                        "Drag me around!",
                        egui::FontId::proportional(11.0),
                        egui::Color32::from_rgba_unmultiplied(255, 255, 255, alpha),
                    );
                }
            });

        // Show welcome message on first frame
        if self.animation_time > 0.5 && self.animation_time < 0.6 && !self.speech_bubble_visible {
            self.speech_bubble_visible = true;
            self.speech_bubble_timer = Some(Instant::now());
            self.character_state = CharacterState::Talking;
        }
    }

    fn clear_color(&self, _visuals: &egui::Visuals) -> [f32; 4] {
        egui::Color32::TRANSPARENT.to_normalized_gamma_f32()
    }
}
