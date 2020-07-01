using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace Identity.ViewModels.User
{
    public class LogInViewModel : ILogInViewModel
    {
        [Required]
        [JsonPropertyName("email")]
        public string Email { get; set; }
        [Required]
        [JsonPropertyName("password")]
        public string Password { get; set; }
    }
}